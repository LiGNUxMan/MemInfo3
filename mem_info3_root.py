#!/usr/bin/env python3

# Version 20250121g 4.1.0c
#
# Autor: Axel O'BRIEN (LiGNUxMan) y ChatGPT
#
# Basado en el cript mem_info.py de P@draigBrady.com

import sys
import os
import psutil
import socket
import time
from datetime import timedelta
from datetime import datetime

# Verificar si el script tiene permisos de root
if os.geteuid() != 0:
    sys.stderr.write("Error: Se requieren permisos de root.\n")
    sys.exit(1)

#Letra normal y bold
BOLD = "\033[1m"
RESET = "\033[0m"

########### Define el intervalo de actualizacion ###########

# 📌 Definir el intervalo de actualización (por defecto es None para ejecución única)
interval = None

# 📌 Si se pasa un argumento, usarlo como intervalo
if len(sys.argv) > 1:
    try:
        interval = int(sys.argv[1])  # Convertir argumento a entero
    except ValueError:
        print("Error: El parámetro debe ser un número natural (segundos).")
        sys.exit(1)

########### Ejecuta el script cada X segundos ###########

def ejecutar_script():
    """ Ejecuta la lógica del script mostrando los valores. """

    # Tamaño de página en KiB
    PAGESIZE = os.sysconf("SC_PAGE_SIZE") / 1024  
    our_pid = os.getpid()  # PID del script actual

    # 📌 Obtener la versión del kernel
    def get_kernel_version():
        with open("/proc/sys/kernel/osrelease") as f:
            version = f.read().strip().split(".")[:3]
            version[2] = version[2].split("-")[0]  # Eliminar sufijos adicionales
            return tuple(map(int, version))

    kernel_version = get_kernel_version()

    with open("/proc/sys/kernel/osrelease") as f:
        kernel_version_long = f.read().strip()

    # 📌 Obtener información de la memoria RAM
    mem = psutil.virtual_memory()

    # 📌 Obtener la memoria total del sistema
    def get_total_system_memory():
        with open("/proc/meminfo") as meminfo:
            for line in meminfo:
                if line.startswith("MemTotal:"):
                    return int(line.split()[1])  # MemTotal está en KB
        return 0

    total_system_memory = get_total_system_memory()

    # 📌 Calcular porcentaje de RAM utilizada
    percent_used = (mem.used / total_system_memory) * 100

    # 📌 Función para convertir valores a unidades legibles (KiB, MiB, GiB, etc.)
    def human(num, power="Ki"):
        powers = ["Ki", "Mi", "Gi", "Ti"]
        while num >= 1024:
            num /= 1024.0
            power = powers[powers.index(power) + 1]
        return "%.2f %sB" % (num, power)

    # 📌 Obtener la memoria compartida de un proceso
    def get_shared_memory(pid):
        try:
            smaps_path = f"/proc/{pid}/smaps"
            if os.path.exists(smaps_path):
                with open(smaps_path) as smaps:
                    return sum(int(line.split()[1]) for line in smaps if "Shared" in line)
            elif (2, 6, 1) <= kernel_version <= (2, 6, 9):
                return 0  # No se puede determinar en este rango de kernels
            else:
                return int(open(f"/proc/{pid}/statm").readline().split()[2]) * PAGESIZE
        except:
            return 0  # Evitar errores si el proceso ya no existe

    # 📌 Obtener uso de memoria de procesos
    cmds, shareds, count = {}, {}, {}

    for line in os.popen("ps -e -o rss=,pid=,comm=").readlines():
        try:
            size, pid, cmd = map(str.strip, line.strip().split(None, 2))
            if int(pid) == our_pid:
                continue  # Omitir este script
            shared = get_shared_memory(pid)
            shareds[cmd] = max(shareds.get(cmd, 0), shared)
            cmds[cmd] = cmds.get(cmd, 0) + int(size) - shared
            count[cmd] = count.get(cmd, 0) + 1
        except:
            continue  # Evitar errores con procesos que desaparecen

    # Sumar la memoria compartida más alta de cada programa
    for cmd in cmds:
        cmds[cmd] += shareds[cmd]

    # Ordenar por consumo de RAM (de menor a mayor)
    sorted_processes = sorted(cmds.items(), key=lambda x: x[1])

    # Calcular totales de memoria
    total_private = sum(cmds[cmd] - shareds[cmd] for cmd in cmds)
    total_shared = sum(shareds.values())
    total_memory = total_private + total_shared

    # 📌 Obtener temperatura de la CPU
    cpu_temp = "N/A"
    temps = psutil.sensors_temperatures()
    if "acpitz" in temps:
        cpu_temp = temps["acpitz"][0].current  # Tomamos el primer valor de "acpitz"

    # 📌 Función para colorear texto según la temperatura de la CPU
    def color_text(text, color):
        colors = {
            "red": "\033[91m",
            "yellow": "\033[93m",
            "reset": "\033[0m"
        }
        return f"{colors[color]}{text}{colors['reset']}"

##########

    # 📌 Obtener uso del CPU y carga del sistema
    cpu_usage = psutil.cpu_percent(interval=1)

    # Obtener la cantidad de núcleos de la CPU
    cpu_count = os.cpu_count()

    # Obtener uso del CPU y carga del sistema
    load1, load5, load15 = os.getloadavg()

    # Colores ANSI para terminal
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    # Función para colorear el Load Average
    def color_load(value):
        if value > cpu_count:  # Más del 100%
            return f"{RED}{value:.2f}{RESET}"
        elif value > cpu_count * 0.75:  # Más del 75%
            return f"{YELLOW}{value:.2f}{RESET}"
        else:
            return f"{value:.2f}"

    # Aplicar colores a los valores de Load Average
    load1_str = color_load(load1)
    load5_str = color_load(load5)
    load15_str = color_load(load15)

##########

    # 📌 Obtener uptime del sistema
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))

    # 📌 Obtener información del disco
    disk = psutil.disk_usage('/')
    disk_total = disk.total / (1024**3)  # Convertir a GB
    disk_used = disk.used / (1024**3)
    disk_percent = disk.percent  # Uso en porcentaje

    # 📌 Obtener cantidad de procesos por estado
    states = {
        "running": 0,
        "sleeping": 0,
        "idle": 0,
        "stopped": 0,
        "zombie": 0,
        "other": 0
    }

    total_processes = 0

    for proc in psutil.process_iter(attrs=['pid', 'status']):
        total_processes += 1
        status = proc.info['status']
    
        if status == psutil.STATUS_RUNNING: #R - Running (Ejecutándose) 🏃
            states["running"] += 1
        elif status == psutil.STATUS_SLEEPING: #S - Sleeping (Durmiendo) 😴
            states["sleeping"] += 1
        elif status == psutil.STATUS_IDLE: #I - Idle (Inactivo) 🛑
            states["idle"] += 1
        elif status == psutil.STATUS_STOPPED: #T - Stopped (Detenido) ✋
            states["stopped"] += 1
        elif status == psutil.STATUS_ZOMBIE: #Z - Zombie ☠️
            states["zombie"] += 1
        else:
            states["other"] += 1 #Otros estados no contemplados

    # 📌 Evaluar precisión de la memoria compartida
    def shared_memory_accuracy():
        if kernel_version[:2] == (2, 4):
            if "Inact_" not in open("/proc/meminfo").read():
                return 1
            return 0
        elif kernel_version[:2] == (2, 6):
            if os.path.exists(f"/proc/{os.getpid()}/smaps"):
                return 1
            if (2, 6, 1) <= kernel_version <= (2, 6, 9):
                return -1
            return 0
        else:
            return 1

    # 📌 Colores ANSI para terminal
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    # 📌 Función para aplicar color según umbral
    def apply_color(value, yellow_threshold, red_threshold, suffix=""):
        if value > red_threshold:
            return f"{RED}{value}{suffix}{RESET}"  # 🔴 Rojo
        elif value > yellow_threshold:
            return f"{YELLOW}{value}{suffix}{RESET}"  # 🟡 Amarillo
        else:
            return f"{value}{suffix}"  # Sin color

    # 📌 Aplicar colores a cada parámetro
    ram_usage_str = apply_color(mem.percent, 75, 90, "%")
    disk_usage_str = apply_color(disk_percent, 80, 90, "%")
    cpu_usage_str = apply_color(cpu_usage, 34, 67, "%")
    cpu_temp_str = apply_color(cpu_temp, 35, 60, "°C")

    # Obtener la fecha y hora actual
    now = datetime.now()

    # Formatear la fecha y hora
    hora_minuto = now.strftime("%H:%M")  # Hora y minuto
    dia_mes_año = now.strftime("%d/%m/%Y")  # Día, mes y año

    # 📌 Imprimir resultados
    print("-" * 59)
    print("Private    + Shared     = RAM used\tProgram")
    print("-" * 59)
    for cmd, size in sorted_processes:
        private_mem = cmds[cmd] - shareds[cmd]
        shared_mem = shareds[cmd]
        total_mem = cmds[cmd]
        print(f"{human(private_mem):>10} + {human(shared_mem):>10} = {human(total_mem):>10}\t{cmd} ({count[cmd]})")
    print("-" * 59)
    print(f"{BOLD}{human(total_private):>10}{RESET} + {BOLD}{human(total_shared):>10}{RESET} = {BOLD}{human(total_memory):>10}{RESET}    TOTAL SYSTEM")
    print("-" * 59)
    print("Private    + Shared     = RAM used\tProgram")
    print("-" * 59)
    print(f"Processes: {BOLD}{total_processes}{RESET} (running={states['running']}, sleeping={states['sleeping']}, idle={states['idle']}, stopped={states['stopped']}, zombie={states['zombie']}, other={states['other']})")
    print(f"Load average:{BOLD} {load1_str} {load5_str} {load15_str}{RESET}")
    print(f"RAM used: {BOLD}{ram_usage_str}{RESET} ({mem.used / (1024**2):.2f} MiB / {mem.total / (1024**2):.2f} MiB)")
    print(f"Disk usage: {BOLD}{disk_usage_str}{RESET} ({disk_used:.2f} GB / {disk_total:.2f} GB)")
    print(f"CPU usage:{BOLD} {cpu_usage_str}{RESET}")
    print(f"CPU temperature:{RESET} {BOLD}{cpu_temp_str}{RESET}")
    print(f"Kernel version:{RESET} {BOLD}{kernel_version_long}{RESET}")  # Mostrar versión completa del kernel
    print(f"Uptime:{RESET} {BOLD}{uptime_str}{RESET} - Time and date: {BOLD}{hora_minuto} {dia_mes_año}{RESET} ")

    # Mostrar advertencias sobre precisión de memoria compartida
    if shared_memory_accuracy() in [-1, 0]:
        sys.stderr.write("Advertencia: La memoria compartida no se reporta correctamente en este sistema.\n")

# 📌 Si NO hay parámetro → ejecutar una vez y salir
if interval is None:
    ejecutar_script()
else:
    # 📌 Si hay un parámetro → ejecutar en bucle cada X segundos
    while True:
        ejecutar_script()  # 🔥 Aquí se ejecuta correctamente en cada iteración
        print(f"Ejecución automática cada {interval} segundos...")
        time.sleep(interval)



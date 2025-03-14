# MemInfo3 (Memory Information 3) v20250121g 4.1.0c

## 🇺🇸🇬🇧 English

## Description

MemInfo3 is a Python script designed to collect and display detailed system information in Linux environments. This script, which must be run with root permissions, provides a comprehensive breakdown of memory usage per process, differentiating between private and shared memory, and also displays key system statistics such as CPU usage and load, temperature, disk usage, uptime, and kernel version.

## Features

- **Memory Information:**
  - Calculates and displays the memory used by each process, differentiating between private and shared memory.
  - Extracts data directly from `/proc/meminfo` to obtain total system memory.

- **System Metrics:**
  - Monitors CPU usage, load average, and CPU temperature.

- Displays disk usage statistics, including total capacity and percentage used.
  - Reports uptime and kernel version.

- **Visualization:**
  - Uses ANSI color codes to highlight critical values ​​(e.g., high resource usage), making it easier to understand.
  - Issues warnings if shared memory is not reported correctly depending on the kernel version.

- **Execution Mode:**
  - Allows you to run the script one-time or continuously, updating the information every X seconds if an interval is provided as an argument.

## Installation and Use

- **Operating System:** Linux (with access to the `/proc` file system).
- **Permissions:** Root permissions are required for proper execution.
- **Python:** Python 3.x.
- **Dependencies:**
- [psutil](https://pypi.org/project/psutil/) (for obtaining system statistics).

## Installation

### Requirements
1. **Verify that you have Python 3 installed.**
2. **Install the psutil dependency:**
    ```bash
    pip install psutil

3. Download the mem_info3_root.py script.

### Execution

Run the script with root permissions. You can choose to run it once or in continuous monitoring mode.

- **Single execution:**

  ```bash
  sudo python3 mem_info3_root.py

- **Continuous execution (monitoring mode):**

  ```bash
  sudo python3 mem_info3_root.py 5
In this case, the information will be updated every 5 seconds.

### Output example

![Captura de pantalla de 2025-03-14 12-51-30](https://github.com/user-attachments/assets/26de45ef-00f4-45b0-8da9-64c5bb5f3f3a)

```
 67.71 MiB +  44.71 MiB = 112.43 MiB	nemo-desktop (1)
 65.80 MiB +  48.10 MiB = 113.90 MiB	guake (1)
 69.64 MiB +  46.18 MiB = 115.82 MiB	nemo (1)
 75.12 MiB +  65.09 MiB = 140.21 MiB	Xorg (1)
 95.33 MiB +  54.23 MiB = 149.56 MiB	mintUpdate (1)
127.65 MiB +  36.85 MiB = 164.50 MiB	xdg-desktop-por (3)
117.58 MiB +  49.52 MiB = 167.11 MiB	xed (1)
257.80 MiB +  22.00 MiB = 279.80 MiB	dropbox (1)
235.39 MiB + 105.07 MiB = 340.46 MiB	cinnamon (1)
  3.06 GiB + 163.43 MiB =   3.21 GiB	chrome (33)
-----------------------------------------------------------
  4.81 GiB +   1.85 GiB =   6.67 GiB    TOTAL SYSTEM
-----------------------------------------------------------
Private    + Shared     = RAM used	Program
-----------------------------------------------------------
Processes: 272 (running=1, sleeping=207, idle=63, stopped=0, zombie=1, other=0)
Load average: 0.38 0.46 0.64
RAM used: 35.3% (4739.82 MiB / 15865.96 MiB)
Disk usage: 45.3% (200.97 GB / 467.91 GB)
CPU usage: 6.5%
CPU temperature: 35.0°C
Kernel version: 6.11.0-19-generic
Uptime: 2 days, 1:14:07 - Time and date: 12:51 14/03/2025 
```

## Contributions
Any improvements, corrections, or suggestions are welcome. Add your contribution to this project!

## Author and Credits
**Author:** Axel O'BRIEN (LiGNUxMan) and ChatGPT.  
**Based on:** The original mem_info.py script for Python 2 by p@draigBrady.com.

## License
This project is distributed under the **GPLv3** license. Feel free to use, modify, and share it!

## Version
**Version:** 20250121g 4.1.0c

## Additional Notes
- The script combines the use of the psutil library with direct reading of files in /proc to gather accurate system data.
- Make sure your system has the necessary permissions and settings to access sensor information and system files.


---
# MemInfo3 (Memory information 3) v20250121g 4.1.0c

## 🇪🇸 Español

## Descripción

MemInfo3 es un script en Python diseñado para recopilar y mostrar información detallada del sistema en entornos Linux. Este script, que debe ejecutarse con permisos de root, ofrece un desglose exhaustivo del uso de memoria por proceso, diferenciando entre memoria privada y compartida, y además muestra estadísticas clave del sistema como el uso y carga del CPU, temperatura, uso del disco, tiempo de actividad y versión del kernel.

## Características

- **Información de Memoria:**
  - Calcula y muestra la memoria utilizada de cada proceso, diferenciando entre la parte privada y la compartida.
  - Extrae datos directamente desde `/proc/meminfo` para obtener la memoria total del sistema.
  
- **Métricas del Sistema:**
  - Monitorea el uso del CPU, la carga promedio (load average) y la temperatura de la CPU.
  - Muestra estadísticas de uso del disco, incluyendo la capacidad total y el porcentaje utilizado.
  - Informa el tiempo de actividad (uptime) y la versión del kernel.

- **Visualización:**
  - Utiliza códigos de color ANSI para resaltar valores críticos (por ejemplo, altos consumos de recursos) facilitando la interpretación visual.
  - Emite advertencias en caso de que la memoria compartida no se reporte correctamente según la versión del kernel.

- **Modo de Ejecución:**
  - Permite ejecutar el script de forma única o en modo continuo, actualizando la información cada X segundos si se proporciona un intervalo como argumento.

## Instalación y Uso

- **Sistema Operativo:** Linux (con acceso al sistema de archivos `/proc`).
- **Permisos:** Se requieren permisos de root para la correcta ejecución.
- **Python:** Python 3.x.
- **Dependencias:** 
  - [psutil](https://pypi.org/project/psutil/) (para la obtención de estadísticas del sistema).

## Instalación

### Requisitos
1. **Verifica que tienes Python 3 instalado.**
2. **Instala la dependencia psutil:**
   ```bash
     pip install psutil

3. Descarga el script mem_info3_root.py.

### Ejecución

Ejecuta el script con permisos de root. Puedes optar por una ejecución única o en modo de monitoreo continuo.

- **Ejecución única:**

    ```bash
    sudo python3 mem_info3_root.py

- **Ejecución continua (modo monitoreo):**

    ```bash
    sudo python3 mem_info3_root.py 5
En este caso, la información se actualizará cada 5 segundos.

### Ejemplo de salida

![Captura de pantalla de 2025-03-14 12-51-30](https://github.com/user-attachments/assets/1d932016-a0ff-4d86-bcb1-25199d60dc67)

```
 67.71 MiB +  44.71 MiB = 112.43 MiB	nemo-desktop (1)
 65.80 MiB +  48.10 MiB = 113.90 MiB	guake (1)
 69.64 MiB +  46.18 MiB = 115.82 MiB	nemo (1)
 75.12 MiB +  65.09 MiB = 140.21 MiB	Xorg (1)
 95.33 MiB +  54.23 MiB = 149.56 MiB	mintUpdate (1)
127.65 MiB +  36.85 MiB = 164.50 MiB	xdg-desktop-por (3)
117.58 MiB +  49.52 MiB = 167.11 MiB	xed (1)
257.80 MiB +  22.00 MiB = 279.80 MiB	dropbox (1)
235.39 MiB + 105.07 MiB = 340.46 MiB	cinnamon (1)
  3.06 GiB + 163.43 MiB =   3.21 GiB	chrome (33)
-----------------------------------------------------------
  4.81 GiB +   1.85 GiB =   6.67 GiB    TOTAL SYSTEM
-----------------------------------------------------------
Private    + Shared     = RAM used	Program
-----------------------------------------------------------
Processes: 272 (running=1, sleeping=207, idle=63, stopped=0, zombie=1, other=0)
Load average: 0.38 0.46 0.64
RAM used: 35.3% (4739.82 MiB / 15865.96 MiB)
Disk usage: 45.3% (200.97 GB / 467.91 GB)
CPU usage: 6.5%
CPU temperature: 35.0°C
Kernel version: 6.11.0-19-generic
Uptime: 2 days, 1:14:07 - Time and date: 12:51 14/03/2025 
```

## Contribuciones
Cualquier mejora, corrección o sugerencia es bienvenida. ¡Suma tu aporte a este proyecto!

## Autor y Créditos
**Autor:** Axel O'BRIEN (LiGNUxMan) y ChatGPT.  
**Basado en:** El script original mem_info.py pata Python2 de p@draigBrady.com.

## Licencia
Este proyecto se distribuye bajo la licencia **GPLv3**. ¡Úsalo, modifícalo y compártelo libremente!

## Versión
**Version:** 20250121g 4.1.0c

## Notas Adicionales
- El script combina el uso de la librería psutil con la lectura directa de archivos en /proc para recopilar datos precisos sobre el sistema.
- Asegúrate de que tu sistema disponga de los permisos y configuraciones necesarias para acceder a la información de sensores y archivos del sistema.

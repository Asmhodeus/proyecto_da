import psutil
import subprocess
import time
import json
from datetime import datetime
import os

# Fecha
fecha = datetime.now().strftime("%Y-%m-%d")
output_path = f"reportes/report_{fecha}.json"

# Crear carpeta si no existe
os.makedirs("reportes", exist_ok=True)

print("Ejecutando Lighthouse...")

# Ejecutar Lighthouse
proceso = subprocess.Popen(
    f'npx lighthouse https://www.bbc.com/'
    f'--output=json '
    f'--output-path="{output_path}" '
    f'--quiet '
    f'--chrome-flags="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage"',
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

cpu_usage = []
ram_usage = []

# Monitoreo mientras corre
while proceso.poll() is None:
    try:
        p = psutil.Process(proceso.pid)
        cpu_usage.append(p.cpu_percent(interval=1))
        ram_usage.append(p.memory_info().rss / (1024 * 1024))  # MB
    except:
        break

# Esperar a que termine completamente
stdout, stderr = proceso.communicate()

# Mostrar errores de Lighthouse si existen
if proceso.returncode != 0:
    print("Error en Lighthouse:")
    print(stderr.decode(errors="ignore"))

# Promedios
cpu_avg = sum(cpu_usage)/len(cpu_usage) if cpu_usage else 0
ram_avg = sum(ram_usage)/len(ram_usage) if ram_usage else 0

print("CPU promedio:", cpu_avg)
print("RAM promedio:", ram_avg)

# Validar que el archivo existe antes de leerlo
if not os.path.exists(output_path):
    print("Error: No se generó el JSON de Lighthouse")
    exit()

# Leer JSON con UTF-8 
try:
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("Error leyendo JSON:", e)
    exit()

# Agregar métricas personalizadas
data["custom_metrics"] = {
    "cpu_avg": cpu_avg,
    "ram_avg_mb": ram_avg
}

# Guardar nuevamente
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Reporte generado correctamente:", output_path)
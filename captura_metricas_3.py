import psutil
import subprocess
import time
import json
from datetime import datetime
import os

# Configuración
URL = "https://www.amazon.com/"
fecha = datetime.now().strftime("%Y-%m-%d")
output_dir = "reportes_3"
output_path = f"{output_dir}/report_{fecha}.json"

# Crear carpeta si no existe
os.makedirs(output_dir, exist_ok=True)

print("Ejecutando Lighthouse...")

# Ejecutar Lighthouse
proceso = subprocess.Popen(
    f'npx lighthouse {URL} '
    f'--output=json '
    f'--output-path="{output_path}" '
    f'--quiet '
    f'--chrome-flags="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage --user-agent=\\"Mozilla/5.0\\""',
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

# Mostrar errores si los hay
if proceso.returncode != 0:
    print("Error en Lighthouse:")
    print(stderr.decode(errors="ignore"))

# Promedios
cpu_avg = sum(cpu_usage)/len(cpu_usage) if cpu_usage else 0
ram_avg = sum(ram_usage)/len(ram_usage) if ram_usage else 0

print("CPU promedio:", cpu_avg)
print("RAM promedio:", ram_avg)

# VALIDACIONES CRÍTICAS

# 1. Validar que el archivo existe
if not os.path.exists(output_path):
    print("Error: No se generó el JSON de Lighthouse")
    exit()

# 2. Validar tamaño mínimo (evita JSON corruptos)
if os.path.getsize(output_path) < 5000:
    print("JSON muy pequeño, probablemente falló Lighthouse")
    exit()

# 3. Leer JSON seguro
try:
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("Error leyendo JSON:", e)
    exit()

# 4. Validar estructura mínima esperada
if "audits" not in data:
    print("JSON inválido: no contiene 'audits'")
    exit()

# Agregar métricas personalizadas
data["custom_metrics"] = {
    "cpu_avg_percent": cpu_avg,
    "ram_avg_mb": ram_avg
}

# Guardar nuevamente
try:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
except Exception as e:
    print("Error guardando JSON:", e)
    exit()

print("✅ Reporte generado correctamente:", output_path)
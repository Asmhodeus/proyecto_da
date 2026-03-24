import psutil
import subprocess
import time
import json
from datetime import datetime

# Fecha
fecha = datetime.now().strftime("%Y-%m-%d")
output_path = f"reportes/report_{fecha}.json"

# Ejecutar Lighthouse
proceso = subprocess.Popen([
    "npx", "lighthouse",
    "https://es.wikipedia.org",
    "--output=json",
    "--output-path=" + output_path
])

cpu_usage = []
ram_usage = []

while proceso.poll() is None:
    try:
        p = psutil.Process(proceso.pid)
        cpu_usage.append(p.cpu_percent(interval=1))
        ram_usage.append(p.memory_info().rss / (1024 * 1024))  # MB
    except:
        break

# Promedios
cpu_avg = sum(cpu_usage)/len(cpu_usage) if cpu_usage else 0
ram_avg = sum(ram_usage)/len(ram_usage) if ram_usage else 0

# 🔥 Guardar en el mismo JSON
with open(output_path, "r") as f:
    data = json.load(f)

data["custom_metrics"] = {
    "cpu_avg": cpu_avg,
    "ram_avg_mb": ram_avg
}

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print("CPU:", cpu_avg)
print("RAM:", ram_avg)
print("Reporte generado:", output_path)
import psutil
import subprocess
import time
import json
from datetime import datetime
import os

# =========================
# CONFIGURACION MULTI PAGINAS
# =========================
targets = [
    {"url": "https://es.wikipedia.org", "dir": "reportes"},
    {"url": "https://www.britannica.com", "dir": "reportes_2"},
    {"url": "https://www.amazon.com", "dir": "reportes_3"},
    {"url": "https://co.ebay.com", "dir": "reportes_4"},
    {"url": "https://www.bbc.com", "dir": "reportes_5"},
    {"url": "https://edition.cnn.com", "dir": "reportes_6"},
    {"url": "https://www.coursera.org", "dir": "reportes_7"},
    {"url": "https://www.edx.org", "dir": "reportes_8"},
    {"url": "https://www.youtube.com", "dir": "reportes_9"},
    {"url": "https://www.dailymotion.com/co", "dir": "reportes_10"},
]

fecha = datetime.now().strftime("%Y-%m-%d")

# =========================
# LOOP PRINCIPAL
# =========================
for target in targets:
    URL = target["url"]
    output_dir = target["dir"]
    output_path = f"{output_dir}/report_{fecha}.json"

    os.makedirs(output_dir, exist_ok=True)

    print(f"\nEjecutando Lighthouse para: {URL}")

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

    while proceso.poll() is None:
        try:
            parent = psutil.Process(proceso.pid)

        # incluir hijos (Chrome)
            processes = [parent] + parent.children(recursive=True)

            cpu_total = 0
            ram_total = 0

            for proc in processes:
                try:
                    cpu_total += proc.cpu_percent(interval=0.5)
                    ram_total += proc.memory_info().rss / (1024 * 1024)
                except:
                    continue

            cpu_usage.append(cpu_total)
            ram_usage.append(ram_total)

        except:
            break

    stdout, stderr = proceso.communicate()

    if proceso.returncode != 0:
        print("⚠️ Error en Lighthouse:")
        print(stderr.decode(errors="ignore"))

    # Promedios
    cpu_avg = sum(cpu_usage)/len(cpu_usage) if cpu_usage else 0
    ram_avg = sum(ram_usage)/len(ram_usage) if ram_usage else 0

    print("CPU:", cpu_avg)
    print("RAM:", ram_avg)

    # =========================
    # VALIDACIONES
    # =========================
    if not os.path.exists(output_path):
        print("❌ No se generó JSON")
        continue

    if os.path.getsize(output_path) < 5000:
        print("❌ JSON inválido (muy pequeño)")
        continue

    try:
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("❌ Error leyendo JSON:", e)
        continue

    if "audits" not in data:
        print("❌ JSON sin audits")
        continue

    # =========================
    # AGREGAR METRICAS
    # =========================
    data["custom_metrics"] = {
        "cpu_avg_percent": cpu_avg,
        "ram_avg_mb": ram_avg
    }

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("❌ Error guardando JSON:", e)
        continue

    print(f"Guardado en {output_path}")

print("\n✅ PROCESO COMPLETO FINALIZADO")
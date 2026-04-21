@echo off

cd /d "D:\Universidad\10mo Semestre\Big data\Proyecto_desempeño_ambiental"

echo Ejecutando captura completa...

python captura_metricas.py
pause
python captura_metricas_2.py
pause
python captura_metricas_3.py
pause
python captura_metricas_4.py
pause
python captura_metricas_5.py
pause
python captura_metricas_6.py
pause
python captura_metricas_7.py
pause
python captura_metricas_8.py
pause
python captura_metricas_9.py
pause
python captura_metricas_10.py
pause

echo Agregando cambios a git...
git add .
echo Haciendo commit...
git commit -m "Reporte %fecha%"
echo Haciendo push...
git push origin master

echo Proceso finalizado
pause
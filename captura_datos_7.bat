@echo off

cd /d "D:\Universidad\10mo Semestre\Big data\Proyecto_desempeño_ambiental"

echo Ejecutando captura completa...

python captura_metricas_7.py

echo Agregando cambios a git...
git add .
echo Haciendo commit...
git commit -m "Reporte %fecha%"
echo Haciendo push...
git push origin master

echo Proceso finalizado
pause
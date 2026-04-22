@echo off

echo Ejecutando captura completa...

cd /d "D:\Universidad\10mo Semestre\Big data\Proyecto_desempeño_ambiental"

python "D:\Universidad\10mo Semestre\Big data\Proyecto_desempeño_ambiental\001_captura_metricas_master.py"

echo Agregando cambios a git...
git add .
echo Haciendo commit...
git commit -m "Reporte %fecha%"
echo Haciendo push...
git push origin master

echo Proceso finalizado
pause
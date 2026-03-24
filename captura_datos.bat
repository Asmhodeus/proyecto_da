@echo off

@echo off

echo Ejecutando captura completa...

python captura_metricas.py

echo Agregando cambios a git...
git add .
echo Haciendo commit...
git commit -m "Reporte %fecha%"
echo Haciendo push...
git push origin master

echo Proceso finalizado
pause
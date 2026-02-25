@echo off

REM Ir al directorio donde está el .bat
cd /d "%~dp0"

set fecha=%random%

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set fecha=%%i

echo Fecha detectada: %fecha%

echo Generando reporte %fecha%...
lighthouse https://es.wikipedia.org --output=json --output-path=reportes/report_%fecha%.json

echo Agregando cambios a git...
git add .
echo Haciendo commit...
git commit -m "Reporte %fecha%"
echo Haciendo push...
git push origin master

pause
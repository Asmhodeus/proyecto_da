@echo off

set fecha=%random%

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set fecha=%%i

echo Fecha detectada: %fecha%

lighthouse https://es.wikipedia.org --output=json --output-path=reportes/report_%fecha%.json

git add .
git commit -a "Reporte %fecha%"
git push origin master

pause
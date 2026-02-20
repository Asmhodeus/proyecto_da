@echo off
set fecha=%date:~10,4%-%date:~4,2%-%date:~7,2%
lighthouse https://es.wikipedia.org --output=json --output-path=./report.json
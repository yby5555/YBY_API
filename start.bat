@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo Starting YBY API Django Server...
python manage.py migrate
python manage.py runserver 0.0.0.0:20125
pause
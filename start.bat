@echo off
echo ============================================
echo   Vibers Olimpiads - Ishga tushirish
echo ============================================
echo.
cd /d "%~dp0"
pip install flask -q
echo Sayt ishga tushmoqda...
echo Brauzerda: http://localhost:5000
echo To'xtatish uchun: Ctrl+C
echo.
python app.py
pause

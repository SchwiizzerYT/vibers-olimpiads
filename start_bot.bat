@echo off
echo ===================================================
echo     Vibers Olimpiads - Telegram Bot (@vibers_result_bot)
echo ===================================================
echo.
cd /d "%~dp0"
python -m pip install pyTelegramBotAPI -q
echo Bot ishga tushmoqda...
echo To'xtatish uchun: Ctrl+C
echo.
python telegram_bot.py
pause

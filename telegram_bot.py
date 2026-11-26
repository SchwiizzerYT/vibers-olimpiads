"""
=============================================================================
             VIBERS OLIMPIADS - TELEGRAM BOT (@vibers_result_bot)
=============================================================================
Ushbu bot saytda foydalanuvchilar olimpiadani yechib topshirganida natijalarni 
avtomatik tarzda @javohircoder0 ga yuboradi va bot orqali natijalarni ko'rish 
imkonini beradi.

O'rnatish:
    pip install pyTelegramBotAPI

Ishga tushirish:
    python telegram_bot.py
=============================================================================
"""

import telebot
from telebot import types
import json
import os
from datetime import datetime

# ==================== SOZLAMALAR ====================
# @BotFather dan olingan @vibers_result_bot tokenini kiriting:
BOT_TOKEN = os.environ.get("VIBERS_BOT_TOKEN", "9240852660:AAF8Ijejj4k_ceAUuGgugvHTzPLZRFQGLzU")

# @javohircoder0 ning Telegram Chat ID raqamini kiriting (masalan: 123456789):
# O'z ID-ingizni @userinfobot yoki @myidbot orqali bilib olishingiz mumkin.
ADMIN_CHAT_ID = os.environ.get("VIBERS_ADMIN_ID", "6791708849")
ADMIN_USERNAME = "@javohircoder0"

# Ma'lumotlar fayllari
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_FILE = os.path.join(DATA_DIR, 'results.json')
OLYMPIADS_FILE = os.path.join(DATA_DIR, 'olympiads.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Yordamchi JSON o'qish funksiyasi
def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

# ==================== NATIJANI @javohircoder0 GA YUBORISH FUNKSIYASI ====================
def notify_admin_about_result(result_info):
    """
    Saytda kimdir test topshirganda ushbu funksiya @javohircoder0 ga xabar yuboradi.
    """
    if BOT_TOKEN == "EXAMPLE_BOT_TOKEN_HERE" or ADMIN_CHAT_ID == "EXAMPLE_CHAT_ID":
        print("[OGOHLANTIRISH] Iltimos BOT_TOKEN va ADMIN_CHAT_ID qiymatlarini kiriting!")
        return False

    message = (
        f"🏆 <b>Yangi Olimpiada Natijasi Qabul Qilindi!</b>\n"
        f"─────────────────────────\n"
        f"👤 <b>Ishtirokchi:</b> {result_info.get('participant_name')}\n"
        f"🏫 <b>Maktab / Hudud:</b> {result_info.get('school')}\n"
        f"🏅 <b>Olimpiada:</b> {result_info.get('olympiad_title')}\n"
        f"🎯 <b>Natija:</b> {result_info.get('correct_count', 0)} / {result_info.get('total_questions', 0)} ta to'g'ri\n"
        f"⭐️ <b>To'plangan ball:</b> <b>{result_info.get('score')} ball</b> ({result_info.get('percentage', 0)}%)\n"
        f"🥇 <b>Egallangan o'rin:</b> {result_info.get('place')}-o'rin\n"
        f"📅 <b>Sana va vaqt:</b> {result_info.get('date')} {result_info.get('time', '')}\n"
        f"─────────────────────────\n"
        f"👨‍💻 <b>Admin:</b> {ADMIN_USERNAME}"
    )

    try:
        bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
        print(f"Xabar muvaffaqiyatli {ADMIN_USERNAME} ({ADMIN_CHAT_ID}) ga yuborildi.")
        return True
    except Exception as e:
        print(f"Xabar yuborishda xatolik yuz berdi: {e}")
        return False

# ==================== BOT BUYRUQLARI ====================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Assalomu alaykum, <b>{user_name}</b>!\n\n"
        f"🤖 Men <b>@vibers_result_bot</b> botiman.\n"
        f"Vibers Olimpiads platformasidagi barcha yangi olimpiada natijalari "
        f"avtomatik tarzda <b>{ADMIN_USERNAME}</b> ga kelib tushadi.\n\n"
        f"<b>Mavjud buyruqlar:</b>\n"
        f"/results - Eng so'nggi olimpiada natijalari\n"
        f"/stats - Platforma statistikasi\n"
        f"/myid - O'zingizning Telegram Chat ID raqamingizni bilish\n"
        f"/test - {ADMIN_USERNAME} ga sinov xabari yuborish"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['myid'])
def send_my_id(message):
    bot.reply_to(message, f"Sizning Telegram Chat ID raqamingiz: <code>{message.chat.id}</code>")

@bot.message_handler(commands=['results'])
def send_results_list(message):
    results = load_json(RESULTS_FILE)
    if not results:
        bot.reply_to(message, "Hozircha hech qanday natijalar mavjud emas.")
        return

    # Oxirgi 10 ta natijani olamiz
    recent = list(reversed(results))[:10]
    text = "📋 <b>So'nggi Olimpiada Natijalari:</b>\n─────────────────────────\n"
    for idx, r in enumerate(recent, 1):
        place_emoji = "🥇" if r.get('place') == 1 else ("🥈" if r.get('place') == 2 else ("🥉" if r.get('place') == 3 else "🎖"))
        text += (
            f"{place_emoji} <b>{r.get('participant_name')}</b> ({r.get('school')})\n"
            f"   Fan/Musobaqa: {r.get('olympiad_title')}\n"
            f"   Ball: <b>{r.get('score')}</b> ({r.get('correct_count')}/{r.get('total_questions')})\n"
            f"   Sana: {r.get('date')} {r.get('time', '')}\n\n"
        )
    bot.reply_to(message, text)

@bot.message_handler(commands=['stats'])
def send_stats(message):
    olympiads = load_json(OLYMPIADS_FILE)
    users = load_json(USERS_FILE)
    results = load_json(RESULTS_FILE)

    text = (
        f"📊 <b>Vibers Olimpiads Statistikasi:</b>\n"
        f"─────────────────────────\n"
        f"🏆 Jami olimpiadalar: <b>{len(olympiads)} ta</b>\n"
        f"👥 Foydalanuvchilar: <b>{len(users)} nafar</b>\n"
        f"📈 Topshirilgan testlar: <b>{len(results)} ta</b>\n"
        f"─────────────────────────\n"
        f"Sayt: http://localhost:5000"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['test'])
def test_notification(message):
    """
    Test maqsadida @javohircoder0 ga xabar yuborish
    """
    if str(message.chat.id) != str(ADMIN_CHAT_ID) and ADMIN_CHAT_ID != "EXAMPLE_CHAT_ID":
        bot.reply_to(message, f"Bu buyruq faqat admin ({ADMIN_USERNAME}) uchun mo'ljallangan.")
        return

    sample_result = {
        "participant_name": "Test Ishtirokchi",
        "school": "1-IDUM, Toshkent",
        "olympiad_title": "Matematika Olimpiadasi",
        "score": 15,
        "total_questions": 3,
        "correct_count": 3,
        "percentage": 100.0,
        "place": 1,
        "date": datetime.now().strftime('%Y-%m-%d'),
        "time": datetime.now().strftime('%H:%M:%S')
    }
    success = notify_admin_about_result(sample_result)
    if success:
        bot.reply_to(message, "✅ Test xabarnomasi muvaffaqiyatli yuborildi!")
    else:
        bot.reply_to(message, "❌ Xatolik yuz berdi. Bot tokeni yoki ADMIN_CHAT_ID ni tekshiring.")

# ==================== BOTNI ISHGA TUSHIRISH ====================
if __name__ == '__main__':
    print("=" * 60)
    print("  @vibers_result_bot Telegram boti ishga tushdi!")
    print(f"  Qabul qiluvchi: {ADMIN_USERNAME} (ID: {ADMIN_CHAT_ID})")
    print("=" * 60)
    
    if BOT_TOKEN == "EXAMPLE_BOT_TOKEN_HERE":
        print("\n[DIQQAT] Haqiqiy bot tokenini BOT_TOKEN ga qo'ying.")
        print("Sayt baribir ishlayveradi (natijalar sayt va admin panelga yoziladi).\n")
    else:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"Botda xatolik: {e}")

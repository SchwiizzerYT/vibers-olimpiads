from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'vibers_olimpiads_secret_key_2024'

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, 'users.json')
OLYMPIADS_FILE = os.path.join(DATA_DIR, 'olympiads.json')
RESULTS_FILE = os.path.join(DATA_DIR, 'results.json')
NEWS_FILE = os.path.join(DATA_DIR, 'news.json')

# Telegram Bot sozlamalari
# @vibers_result_bot uchun token va @javohircoder0 ning Telegram ID si
TELEGRAM_BOT_TOKEN = os.environ.get("VIBERS_BOT_TOKEN", "9240852660:AAF8Ijejj4k_ceAUuGgugvHTzPLZRFQGLzU")
# @javohircoder0 ning telegram chat ID si (masalan raqam: 123456789)
TELEGRAM_ADMIN_CHAT_ID = os.environ.get("VIBERS_ADMIN_ID", "6791708849")

def send_telegram_result(result_info):
    """
    Natija topshirilganda @javohircoder0 ga @vibers_result_bot orqali xabar yuborish
    """
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "EXAMPLE_BOT_TOKEN_HERE":
        print("[Telegram Notification] Bot tokeni o'rnatilmagan (EXAMPLE_BOT_TOKEN_HERE). Xabar konsolga chiqarildi:")
        print(f"Yangi natija: {result_info.get('participant_name')} - {result_info.get('olympiad_title')}: {result_info.get('score')} ball")
        return False

    message = (
        f"🏆 <b>Yangi Olimpiada Natijasi!</b> (@vibers_result_bot)\n\n"
        f"👤 <b>Ishtirokchi:</b> {result_info.get('participant_name')}\n"
        f"🏫 <b>Maktab / Tashkilot:</b> {result_info.get('school')}\n"
        f"🏅 <b>Olimpiada:</b> {result_info.get('olympiad_title')}\n"
        f"🎯 <b>Natija:</b> {result_info.get('correct_count', 0)} / {result_info.get('total_questions', 0)} ta to'g'ri\n"
        f"⭐️ <b>To'plangan ball:</b> {result_info.get('score')} ball ({result_info.get('percentage', 0)}%)\n"
        f"📅 <b>Sana va vaqt:</b> {result_info.get('date')} {result_info.get('time', '')}\n\n"
        f"👨‍💻 <b>Qabul qiluvchi:</b> @javohircoder0"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_ADMIN_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except Exception as e:
        print(f"[Telegram Error] Xabar yuborishda xatolik: {e}")
        return False

# Initialize data files
def init_data():
    if not os.path.exists(USERS_FILE):
        users = [
            {
                "id": 1,
                "username": "admin_1336",
                "password": "1234recource1234",
                "role": "admin",
                "full_name": "Administrator",
                "email": "admin@vibers.uz",
                "created_at": "2024-01-01"
            }
        ]
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    if not os.path.exists(OLYMPIADS_FILE):
        olympiads = [
            {
                "id": 1,
                "title": "Matematika Olimpiadasi",
                "subject": "Matematika",
                "level": "Respublika",
                "date": "2024-03-15",
                "deadline": "2024-03-01",
                "description": "Respublika matematika olimpiadasi 7-11 sinf o'quvchilari uchun",
                "status": "active",
                "participants": 0,
                "image": "math.png",
                "questions": [
                    {
                        "id": 1,
                        "question": "2x + 6 = 14 bo'lsa, x ning qiymatini toping:",
                        "option_a": "3",
                        "option_b": "4",
                        "option_c": "5",
                        "option_d": "6",
                        "correct_option": "B",
                        "points": 5
                    },
                    {
                        "id": 2,
                        "question": "Uchburchakning ichki burchaklari yig'indisi necha gradusga teng?",
                        "option_a": "90°",
                        "option_b": "180°",
                        "option_c": "270°",
                        "option_d": "360°",
                        "correct_option": "B",
                        "points": 5
                    },
                    {
                        "id": 3,
                        "question": "15 ning kvadratini toping (15²):",
                        "option_a": "125",
                        "option_b": "205",
                        "option_c": "225",
                        "option_d": "250",
                        "correct_option": "C",
                        "points": 5
                    }
                ]
            },
            {
                "id": 2,
                "title": "Fizika Olimpiadasi",
                "subject": "Fizika",
                "level": "Viloyat",
                "date": "2024-03-20",
                "deadline": "2024-03-05",
                "description": "Viloyat fizika olimpiadasi 9-11 sinf o'quvchilari uchun",
                "status": "active",
                "participants": 0,
                "image": "physics.png",
                "questions": [
                    {
                        "id": 1,
                        "question": "Nyutonning 2-qonuni formulasi qaysi?",
                        "option_a": "F = m * a",
                        "option_b": "E = mc²",
                        "option_c": "P = F / S",
                        "option_d": "v = s / t",
                        "correct_option": "A",
                        "points": 5
                    }
                ]
            },
            {
                "id": 3,
                "title": "Informatika Olimpiadasi",
                "subject": "Informatika",
                "level": "Xalqaro",
                "date": "2024-04-10",
                "deadline": "2024-03-20",
                "description": "Xalqaro informatika olimpiadasi barcha sinf o'quvchilari uchun",
                "status": "upcoming",
                "participants": 0,
                "image": "it.png",
                "questions": []
            }
        ]
        with open(OLYMPIADS_FILE, 'w', encoding='utf-8') as f:
            json.dump(olympiads, f, ensure_ascii=False, indent=2)

    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    if not os.path.exists(NEWS_FILE):
        news = [
            {
                "id": 1,
                "title": "Vibers Olimpiads platformasi ochildi!",
                "content": "O'zbekiston o'quvchilari uchun yangi olimpiad platformasi muvaffaqiyatli ishga tushirildi.",
                "date": "2024-01-15",
                "author": "Administrator"
            },
            {
                "id": 2,
                "title": "2024-yil olimpiad jadvali e'lon qilindi",
                "content": "2024-yil uchun barcha fanlar bo'yicha olimpiad jadvali tasdiqlandi va e'lon qilindi.",
                "date": "2024-01-20",
                "author": "Administrator"
            }
        ]
        with open(NEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=2)

# Helper functions
def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_next_id(items):
    if not items:
        return 1
    return max(item['id'] for item in items) + 1

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Iltimos, avval tizimga kiring!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Bu sahifaga kirish huquqingiz yo\'q!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/')
def index():
    olympiads = load_json(OLYMPIADS_FILE)
    news = load_json(NEWS_FILE)
    active_olympiads = [o for o in olympiads if o.get('status') == 'active']
    return render_template('index.html', olympiads=active_olympiads[:6], news=news[:3])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        users = load_json(USERS_FILE)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            flash(f'Xush kelibsiz, {user["full_name"]}!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Username yoki parol noto\'g\'ri!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()

        users = load_json(USERS_FILE)

        if not all([username, password, confirm, full_name, email]):
            flash('Barcha maydonlarni to\'ldiring!', 'danger')
        elif password != confirm:
            flash('Parollar mos kelmadi!', 'danger')
        elif len(password) < 6:
            flash('Parol kamida 6 ta belgidan iborat bo\'lishi kerak!', 'danger')
        elif any(u['username'] == username for u in users):
            flash('Bu username allaqachon mavjud!', 'danger')
        elif any(u['email'] == email for u in users):
            flash('Bu email allaqachon ro\'yxatdan o\'tgan!', 'danger')
        else:
            new_user = {
                "id": get_next_id(users),
                "username": username,
                "password": password,
                "role": "user",
                "full_name": full_name,
                "email": email,
                "created_at": datetime.now().strftime('%Y-%m-%d')
            }
            users.append(new_user)
            save_json(USERS_FILE, users)
            flash('Ro\'yxatdan muvaffaqiyatli o\'tdingiz! Endi tizimga kiring.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Tizimdan chiqildi.', 'info')
    return redirect(url_for('index'))

@app.route('/olympiads')
def olympiads():
    all_olympiads = load_json(OLYMPIADS_FILE)
    subject = request.args.get('subject', '')
    level = request.args.get('level', '')
    if subject:
        all_olympiads = [o for o in all_olympiads if o.get('subject') == subject]
    if level:
        all_olympiads = [o for o in all_olympiads if o.get('level') == level]
    return render_template('olympiads.html', olympiads=all_olympiads)

@app.route('/olympiad/<int:oid>')
def olympiad_detail(oid):
    olympiads = load_json(OLYMPIADS_FILE)
    olympiad = next((o for o in olympiads if o['id'] == oid), None)
    if not olympiad:
        flash('Olimpiad topilmadi!', 'danger')
        return redirect(url_for('olympiads'))
    return render_template('olympiad_detail.html', olympiad=olympiad)

# ============ OLIMPIADANI TOPSHIRISH / YECHISH ============
@app.route('/olympiad/<int:oid>/solve', methods=['GET'])
@login_required
def solve_olympiad(oid):
    olympiads = load_json(OLYMPIADS_FILE)
    olympiad = next((o for o in olympiads if o['id'] == oid), None)
    if not olympiad:
        flash('Olimpiada topilmadi!', 'danger')
        return redirect(url_for('olympiads'))
    
    if olympiad.get('status') != 'active':
        flash('Bu olimpiada hozir faol emas!', 'warning')
        return redirect(url_for('olympiad_detail', oid=oid))
    
    questions = olympiad.get('questions', [])
    if not questions:
        flash('Ushbu olimpiadaga hali savollar kiritilmagan!', 'info')
        return redirect(url_for('olympiad_detail', oid=oid))
    
    return render_template('solve_olympiad.html', olympiad=olympiad, questions=questions)

@app.route('/olympiad/<int:oid>/submit', methods=['POST'])
@login_required
def submit_olympiad(oid):
    olympiads = load_json(OLYMPIADS_FILE)
    olympiad = next((o for o in olympiads if o['id'] == oid), None)
    if not olympiad:
        flash('Olimpiada topilmadi!', 'danger')
        return redirect(url_for('olympiads'))
    
    questions = olympiad.get('questions', [])
    if not questions:
        flash('Savollar topilmadi!', 'danger')
        return redirect(url_for('olympiads'))
    
    total_questions = len(questions)
    correct_count = 0
    total_score = 0
    max_score = sum(int(q.get('points', 5)) for q in questions)
    
    user_answers = {}
    for q in questions:
        qid = str(q['id'])
        chosen = request.form.get(f"question_{qid}", "").strip().upper()
        user_answers[qid] = chosen
        if chosen == q.get('correct_option', '').upper():
            correct_count += 1
            total_score += int(q.get('points', 5))
            
    percentage = round((total_score / max_score * 100), 1) if max_score > 0 else 0
    
    # Ishtirokchilar sonini 1 taga oshiramiz
    olympiad['participants'] = olympiad.get('participants', 0) + 1
    save_json(OLYMPIADS_FILE, olympiads)
    
    # Natijani saqlaymiz
    results = load_json(RESULTS_FILE)
    user_school = request.form.get('school', '').strip() or 'Noma\'lum maktab'
    
    # O'rinni ball bo'yicha hisoblash
    place = 1
    if percentage >= 90:
        place = 1
    elif percentage >= 75:
        place = 2
    elif percentage >= 60:
        place = 3
    else:
        place = 4
        
    now = datetime.now()
    new_result = {
        "id": get_next_id(results),
        "user_id": session.get('user_id'),
        "participant_name": session.get('full_name', 'Foydalanuvchi'),
        "school": user_school,
        "olympiad_id": olympiad['id'],
        "olympiad_title": olympiad['title'],
        "score": total_score,
        "max_score": max_score,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "percentage": percentage,
        "place": place,
        "date": now.strftime('%Y-%m-%d'),
        "time": now.strftime('%H:%M:%S')
    }
    results.append(new_result)
    save_json(RESULTS_FILE, results)
    
    # Telegram bot orqali @javohircoder0 ga xabar yuborish
    send_telegram_result(new_result)
    
    flash(f'Olimpiada yakunlandi! Natijangiz: {correct_count}/{total_questions} to\'g\'ri javob ({total_score} ball). Natijangiz admin panelga yuborildi!', 'success')
    return redirect(url_for('results'))

@app.route('/results')
def results():
    all_results = load_json(RESULTS_FILE)
    # Ball bo'yicha saralash
    sorted_results = sorted(all_results, key=lambda x: x.get('score', 0), reverse=True)
    return render_template('results.html', results=sorted_results)

@app.route('/news')
def news():
    all_news = load_json(NEWS_FILE)
    return render_template('news.html', news=all_news)

@app.route('/profile')
@login_required
def profile():
    users = load_json(USERS_FILE)
    user = next((u for u in users if u['id'] == session['user_id']), None)
    results = load_json(RESULTS_FILE)
    user_results = [r for r in results if r.get('user_id') == session['user_id']]
    return render_template('profile.html', user=user, user_results=user_results)

# ============ ADMIN PANEL ============
@app.route('/admin')
@admin_required
def admin_dashboard():
    users = load_json(USERS_FILE)
    olympiads = load_json(OLYMPIADS_FILE)
    results = load_json(RESULTS_FILE)
    news = load_json(NEWS_FILE)
    stats = {
        'users': len(users),
        'olympiads': len(olympiads),
        'active': len([o for o in olympiads if o.get('status') == 'active']),
        'results': len(results),
        'news': len(news)
    }
    return render_template('admin/dashboard.html', stats=stats)

# Admin - Users
@app.route('/admin/users')
@admin_required
def admin_users():
    users = load_json(USERS_FILE)
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/delete/<int:uid>', methods=['POST'])
@admin_required
def admin_delete_user(uid):
    users = load_json(USERS_FILE)
    users = [u for u in users if u['id'] != uid]
    save_json(USERS_FILE, users)
    flash('Foydalanuvchi o\'chirildi!', 'success')
    return redirect(url_for('admin_users'))

# Admin - Olympiads
@app.route('/admin/olympiads')
@admin_required
def admin_olympiads():
    olympiads = load_json(OLYMPIADS_FILE)
    return render_template('admin/olympiads.html', olympiads=olympiads)

@app.route('/admin/olympiads/add', methods=['GET', 'POST'])
@admin_required
def admin_add_olympiad():
    if request.method == 'POST':
        olympiads = load_json(OLYMPIADS_FILE)
        new_o = {
            "id": get_next_id(olympiads),
            "title": request.form.get('title'),
            "subject": request.form.get('subject'),
            "level": request.form.get('level'),
            "date": request.form.get('date'),
            "deadline": request.form.get('deadline'),
            "description": request.form.get('description'),
            "status": request.form.get('status', 'upcoming'),
            "participants": 0,
            "image": "default.png",
            "questions": []
        }
        olympiads.append(new_o)
        save_json(OLYMPIADS_FILE, olympiads)
        flash('Olimpiad qo\'shildi! Endi unga savollarni kiritishingiz mumkin.', 'success')
        return redirect(url_for('admin_edit_olympiad', oid=new_o['id']))
    return render_template('admin/add_olympiad.html')

@app.route('/admin/olympiads/edit/<int:oid>', methods=['GET', 'POST'])
@admin_required
def admin_edit_olympiad(oid):
    olympiads = load_json(OLYMPIADS_FILE)
    olympiad = next((o for o in olympiads if o['id'] == oid), None)
    if not olympiad:
        flash('Olimpiad topilmadi!', 'danger')
        return redirect(url_for('admin_olympiads'))
    
    if request.method == 'POST':
        for o in olympiads:
            if o['id'] == oid:
                o['title'] = request.form.get('title')
                o['subject'] = request.form.get('subject')
                o['level'] = request.form.get('level')
                o['date'] = request.form.get('date')
                o['deadline'] = request.form.get('deadline')
                o['description'] = request.form.get('description')
                o['status'] = request.form.get('status')
                break
        save_json(OLYMPIADS_FILE, olympiads)
        flash('Olimpiad muvaffaqiyatli yangilandi!', 'success')
        return redirect(url_for('admin_edit_olympiad', oid=oid))
        
    return render_template('admin/edit_olympiad.html', olympiad=olympiad)

# Admin - Savol qo'shish
@app.route('/admin/olympiads/<int:oid>/questions/add', methods=['POST'])
@admin_required
def admin_add_question(oid):
    olympiads = load_json(OLYMPIADS_FILE)
    olympiad = next((o for o in olympiads if o['id'] == oid), None)
    if not olympiad:
        flash('Olimpiada topilmadi!', 'danger')
        return redirect(url_for('admin_olympiads'))
    
    if 'questions' not in olympiad:
        olympiad['questions'] = []
        
    new_q_id = 1
    if olympiad['questions']:
        new_q_id = max(q.get('id', 0) for q in olympiad['questions']) + 1
        
    question_data = {
        "id": new_q_id,
        "question": request.form.get('question_text', '').strip(),
        "option_a": request.form.get('option_a', '').strip(),
        "option_b": request.form.get('option_b', '').strip(),
        "option_c": request.form.get('option_c', '').strip(),
        "option_d": request.form.get('option_d', '').strip(),
        "correct_option": request.form.get('correct_option', 'A').strip().upper(),
        "points": int(request.form.get('points', 5))
    }
    
    olympiad['questions'].append(question_data)
    save_json(OLYMPIADS_FILE, olympiads)
    flash(f'{new_q_id}-savol muvaffaqiyatli qo\'shildi!', 'success')
    return redirect(url_for('admin_edit_olympiad', oid=oid))

# Admin - Savolni o'chirish
@app.route('/admin/olympiads/<int:oid>/questions/delete/<int:qid>', methods=['POST'])
@admin_required
def admin_delete_question(oid, qid):
    olympiads = load_json(OLYMPIADS_FILE)
    olympiad = next((o for o in olympiads if o['id'] == oid), None)
    if not olympiad:
        flash('Olimpiada topilmadi!', 'danger')
        return redirect(url_for('admin_olympiads'))
    
    olympiad['questions'] = [q for q in olympiad.get('questions', []) if q.get('id') != qid]
    save_json(OLYMPIADS_FILE, olympiads)
    flash('Savol muvaffaqiyatli o\'chirildi!', 'success')
    return redirect(url_for('admin_edit_olympiad', oid=oid))

@app.route('/admin/olympiads/delete/<int:oid>', methods=['POST'])
@admin_required
def admin_delete_olympiad(oid):
    olympiads = load_json(OLYMPIADS_FILE)
    olympiads = [o for o in olympiads if o['id'] != oid]
    save_json(OLYMPIADS_FILE, olympiads)
    flash('Olimpiad o\'chirildi!', 'success')
    return redirect(url_for('admin_olympiads'))

# Admin - Results
@app.route('/admin/results')
@admin_required
def admin_results():
    results = load_json(RESULTS_FILE)
    # Yangi natijalar tepada bo'lishi uchun teskari tartibda
    results_sorted = sorted(results, key=lambda x: x.get('id', 0), reverse=True)
    return render_template('admin/results.html', results=results_sorted)

@app.route('/admin/results/add', methods=['GET', 'POST'])
@admin_required
def admin_add_result():
    if request.method == 'POST':
        results = load_json(RESULTS_FILE)
        olympiads = load_json(OLYMPIADS_FILE)
        oid = int(request.form.get('olympiad_id'))
        o_title = next((o['title'] for o in olympiads if o['id'] == oid), '')
        now = datetime.now()
        new_r = {
            "id": get_next_id(results),
            "olympiad_id": oid,
            "olympiad_title": o_title,
            "participant_name": request.form.get('participant_name'),
            "school": request.form.get('school'),
            "place": int(request.form.get('place')),
            "score": float(request.form.get('score')),
            "correct_count": int(request.form.get('score')),
            "total_questions": int(request.form.get('score')),
            "percentage": 100,
            "date": now.strftime('%Y-%m-%d'),
            "time": now.strftime('%H:%M:%S')
        }
        results.append(new_r)
        save_json(RESULTS_FILE, results)
        
        # Telegramga ham xabar berish
        send_telegram_result(new_r)
        
        flash('Natija qo\'shildi va @javohircoder0 ga xabar yuborildi!', 'success')
        return redirect(url_for('admin_results'))
    olympiads = load_json(OLYMPIADS_FILE)
    return render_template('admin/add_result.html', olympiads=olympiads)

@app.route('/admin/results/delete/<int:rid>', methods=['POST'])
@admin_required
def admin_delete_result(rid):
    results = load_json(RESULTS_FILE)
    results = [r for r in results if r['id'] != rid]
    save_json(RESULTS_FILE, results)
    flash('Natija o\'chirildi!', 'success')
    return redirect(url_for('admin_results'))

# Admin - News
@app.route('/admin/news')
@admin_required
def admin_news():
    news = load_json(NEWS_FILE)
    return render_template('admin/news.html', news=news)

@app.route('/admin/news/add', methods=['GET', 'POST'])
@admin_required
def admin_add_news():
    if request.method == 'POST':
        news = load_json(NEWS_FILE)
        new_n = {
            "id": get_next_id(news),
            "title": request.form.get('title'),
            "content": request.form.get('content'),
            "date": datetime.now().strftime('%Y-%m-%d'),
            "author": session['full_name']
        }
        news.append(new_n)
        save_json(NEWS_FILE, news)
        flash('Yangilik qo\'shildi!', 'success')
        return redirect(url_for('admin_news'))
    return render_template('admin/add_news.html')

@app.route('/admin/news/delete/<int:nid>', methods=['POST'])
@admin_required
def admin_delete_news(nid):
    news = load_json(NEWS_FILE)
    news = [n for n in news if n['id'] != nid]
    save_json(NEWS_FILE, news)
    flash('Yangilik o\'chirildi!', 'success')
    return redirect(url_for('admin_news'))

if __name__ == '__main__':
    init_data()
    app.run(debug=True, port=5000)

# 🏆 Vibers Olimpiads

O'zbekiston o'quvchilari uchun zamonaviy online olimpiada platformasi. Ushbu tizim orqali o'quvchilar fanlar bo'yicha test sinovlaridan o'tishlari, real vaqtda natijalarini ko'rishlari va Telegram bot orqali natijalarni adminlarga avtomatik yuborishlari mumkin.

## 🚀 Asosiy Imkoniyatlar

- **Olimpiadalar**: Faol, kutilayotgan va yakunlangan olimpiadalar ro'yxati, fanlar va darajalar bo'yicha filtrlash.
- **Online Test Yechish**: O'quvchilar test savollarini online topshirishadi, tizim avtomatik ball va foizni hisoblaydi.
- **Admin Panel**:
  - Olimpiadalar yaratish, tahrirlash, o'chirish.
  - Savollar va variantlar (A, B, C, D) kiritish, to'g'ri javob va ball belgilash.
  - Natijalar monitoringi va yangiliklar e'lon qilish.
- **Telegram Bot Integratsiyasi**:
  - `@vibers_result_bot` boti orqali har bir yangi olimpiada natijasi administrator (`@javohircoder0`) ga avtomatik tarzda kelib tushadi.

---

## 🛠 Texnologiyalar

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Inter font, FontAwesome 6)
- **Ma'lumotlar bazasi**: JSON (users, olympiads, results, news)
- **Telegram Bot**: pyTelegramBotAPI

---

## 📦 O'rnatish va Ishga Tushirish

### 1. Talablar
- Python 3.10+
- Pip paketlar boshqaruvchisi

### 2. O'rnatish
```bash
git clone https://github.com/SchwiizzerYT/vibers-olimpiads.git
cd vibers-olimpiads
pip install -r requirements.txt
```

### 3. Veb-saytni ishga tushirish
```bash
python app.py
```
Yoki Windowsda `start.bat` faylini ikki marta bosing. Sayt `http://localhost:5000` da ochiladi.

### 4. Telegram botni ishga tushirish
```bash
python telegram_bot.py
```
Yoki Windowsda `start_bot.bat` faylini bosing.

---

## 🔐 Standart Admin Ma'lumotlari
- **Kirish sahifasi**: `http://localhost:5000/login`
- **Username**: `admin_1336`
- **Parol**: `1234recource1234`

---

## 👨‍💻 Muallif
- **GitHub**: [@SchwiizzerYT](https://github.com/SchwiizzerYT)
- **Email**: `javalaradash@gmail.com`
- **Telegram**: [@javohircoder0](https://t.me/javohircoder0)

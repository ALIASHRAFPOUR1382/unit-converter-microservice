# راهنمای اجرای سیستم (بدون Docker)

## روش ساده (پیشنهادی)

### گام 1: باز کردن PowerShell
- در پوشه پروژه (`cs_project`) راست کلیک کنید
- "Open in Terminal" یا "Open PowerShell window here" را انتخاب کنید

### گام 2: اجرای اسکریپت
```powershell
.\run.ps1
```

این اسکریپت به صورت خودکار:
- Virtual environment را ایجاد می‌کند (اگر وجود نداشته باشد)
- Dependencies را نصب می‌کند
- فایل `.env` را ایجاد می‌کند (اگر وجود نداشته باشد)
- سرور را اجرا می‌کند

### گام 3: استفاده از API
بعد از اجرا، می‌توانید به آدرس‌های زیر دسترسی داشته باشید:
- **API Documentation**: http://localhost:8000/docs
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

---

## روش دستی (اگر اسکریپت کار نکرد)

### گام 1: ایجاد Virtual Environment
```powershell
python -m venv venv
```

### گام 2: فعال‌سازی Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### گام 3: نصب Dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### گام 4: ایجاد فایل .env (اگر وجود ندارد)
```powershell
# فایل .env را ایجاد کنید و این محتوا را در آن قرار دهید:
DATABASE_URL=sqlite:///./tododb.db
```

یا از فایل `env.example` کپی کنید:
```powershell
Copy-Item env.example .env
```

### گام 5: اجرای سرور
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## توقف سرور

برای توقف سرور، در ترمینال `Ctrl+C` را فشار دهید.

---

## عیب‌یابی

### مشکل: Execution Policy Error
اگر خطای Execution Policy دریافت کردید:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### مشکل: Python پیدا نشد
- مطمئن شوید Python نصب شده است
- Python را به PATH اضافه کنید

### مشکل: Port 8000 در حال استفاده است
اگر پورت 8000 در حال استفاده است، می‌توانید پورت دیگری استفاده کنید:
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

---

## نکات مهم

1. **SQLite**: سیستم به صورت پیش‌فرض از SQLite استفاده می‌کند (نیازی به نصب PostgreSQL نیست)
2. **Auto-reload**: با flag `--reload`، تغییرات در کد به صورت خودکار اعمال می‌شود
3. **Database**: فایل دیتابیس (`tododb.db`) به صورت خودکار ایجاد می‌شود

---

## تست سریع

بعد از اجرا، می‌توانید با مرورگر به آدرس زیر بروید:
```
http://localhost:8000/docs
```

این صفحه Swagger UI است که می‌توانید تمام API endpoints را تست کنید.



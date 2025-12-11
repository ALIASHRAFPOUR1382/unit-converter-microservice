# To-Do App Backend API

یک API کامل و قدرتمند برای مدیریت لیست وظایف (To-Do List) با قابلیت‌های CRUD کامل، pagination، filtering و sorting.

## 📋 فهرست مطالب

- [معرفی پروژه](#معرفی-پروژه)
- [تکنولوژی‌های استفاده شده](#تکنولوژی‌های-استفاده-شده)
- [ساختار پروژه](#ساختار-پروژه)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
- [استفاده از API](#استفاده-از-api)
- [Docker](#docker)
- [Git Workflow](#git-workflow)
- [مستندات API](#مستندات-api)

## 🎯 معرفی پروژه

این پروژه یک سرویس Backend کامل برای مدیریت لیست وظایف است که شامل عملیات CRUD (Create, Read, Update, Delete) می‌باشد. این API با استفاده از FastAPI ساخته شده و از PostgreSQL به عنوان پایگاه داده استفاده می‌کند.

### ویژگی‌های اصلی

- ✅ عملیات CRUD کامل
- 📄 Pagination برای لیست وظایف
- 🔍 Filtering بر اساس وضعیت انجام
- 📊 Sorting بر اساس تاریخ ایجاد
- 🐳 Docker و Docker Compose برای استقرار آسان
- 📚 مستندات خودکار API (Swagger UI)
- 🔒 Validation کامل داده‌ها
- ⚡ Performance بالا با FastAPI

## 🛠 تکنولوژی‌های استفاده شده

- **FastAPI**: فریمورک مدرن و سریع برای ساخت API
- **PostgreSQL**: پایگاه داده رابطه‌ای قدرتمند
- **SQLAlchemy**: ORM برای Python
- **Pydantic**: اعتبارسنجی و serialization داده‌ها
- **Docker & Docker Compose**: Containerization
- **Uvicorn**: ASGI server برای FastAPI

## 📁 ساختار پروژه

```
cs_project/
├── .git/
├── .gitignore
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py              # FastAPI application
    ├── database.py          # Database connection & session
    ├── models.py            # SQLAlchemy models
    ├── schemas.py           # Pydantic schemas
    ├── crud.py              # CRUD operations
    └── routers/
        ├── __init__.py
        └── todos.py         # Todo API endpoints
```

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.11 یا بالاتر
- Docker و Docker Compose (برای استقرار با Docker)
- PostgreSQL (اگر می‌خواهید بدون Docker اجرا کنید)

### روش 1: استفاده از Docker (پیشنهادی)

1. کلون کردن پروژه:
```bash
git clone <repository-url>
cd cs_project
```

2. اجرای با Docker Compose:
```bash
docker-compose up --build
```

این دستور:
- PostgreSQL را راه‌اندازی می‌کند
- اپلیکیشن FastAPI را build و اجرا می‌کند
- جداول دیتابیس را به صورت خودکار ایجاد می‌کند

3. دسترسی به API:
- API: http://localhost:8000
- مستندات Swagger: http://localhost:8000/docs
- مستندات ReDoc: http://localhost:8000/redoc

### روش 2: نصب محلی

1. ایجاد virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # در Windows: venv\Scripts\activate
```

2. نصب dependencies:
```bash
pip install -r requirements.txt
```

3. تنظیم دیتابیس:
   - PostgreSQL را نصب و راه‌اندازی کنید
   - یک دیتابیس با نام `tododb` ایجاد کنید
   - متغیر محیطی `DATABASE_URL` را تنظیم کنید:
   ```bash
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/tododb"
   ```

4. اجرای اپلیکیشن:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 استفاده از API

### Endpoints اصلی

#### 1. ایجاد Todo جدید
```bash
POST /api/todos
Content-Type: application/json

{
  "title": "یادگیری FastAPI",
  "description": "مطالعه مستندات FastAPI",
  "completed": false
}
```

#### 2. دریافت لیست Todos
```bash
GET /api/todos?page=1&page_size=10&completed=false
```

پارامترهای query:
- `page`: شماره صفحه (پیش‌فرض: 1)
- `page_size`: تعداد آیتم در هر صفحه (پیش‌فرض: 10، حداکثر: 100)
- `completed`: فیلتر بر اساس وضعیت (true/false/null برای همه)

#### 3. دریافت یک Todo
```bash
GET /api/todos/{id}
```

#### 4. به‌روزرسانی کامل Todo (PUT)
```bash
PUT /api/todos/{id}
Content-Type: application/json

{
  "title": "یادگیری FastAPI - به‌روزرسانی شده",
  "description": "تکمیل شده",
  "completed": true
}
```

#### 5. به‌روزرسانی جزئی Todo (PATCH)
```bash
PATCH /api/todos/{id}
Content-Type: application/json

{
  "completed": true
}
```

#### 6. حذف Todo
```bash
DELETE /api/todos/{id}
```

#### 7. Health Check
```bash
GET /health
```

### مثال‌های استفاده با curl

```bash
# ایجاد Todo جدید
curl -X POST "http://localhost:8000/api/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "خرید کتاب",
    "description": "خرید کتاب Python",
    "completed": false
  }'

# دریافت لیست Todos
curl "http://localhost:8000/api/todos?page=1&page_size=10"

# دریافت یک Todo
curl "http://localhost:8000/api/todos/1"

# به‌روزرسانی Todo
curl -X PATCH "http://localhost:8000/api/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# حذف Todo
curl -X DELETE "http://localhost:8000/api/todos/1"
```

## 🐳 Docker

### دستورات مفید Docker

```bash
# اجرای سرویس‌ها
docker-compose up

# اجرا در background
docker-compose up -d

# توقف سرویس‌ها
docker-compose down

# توقف و حذف volumes
docker-compose down -v

# مشاهده لاگ‌ها
docker-compose logs -f app

# rebuild کردن
docker-compose up --build
```

## 🔄 Git Workflow

این پروژه از Git workflow با feature branches استفاده می‌کند:

### Feature Branches

- `feature/database-setup`: پیاده‌سازی لایه دیتابیس
- `feature/api-endpoints`: پیاده‌سازی API endpoints
- `feature/docker-setup`: تنظیمات Docker

### Pull Requests

برای ادغام کدها به شاخه اصلی (`main` یا `master`)، از Pull Requests استفاده می‌شود.

### کامیت‌ها

کامیت‌ها باید شفاف و گویا باشند و پیشرفت تدریجی پروژه را نشان دهند.

### سیستم Commit تدریجی

این پروژه شامل یک سیستم commit خودکار برای به‌روزرسانی تدریجی است:

#### استفاده سریع

**Windows (PowerShell):**
```powershell
# Commit خودکار با پیام پیش‌فرض
.\auto-commit.ps1

# Commit با پیام سفارشی و push
.\auto-commit.ps1 -Message "اضافه کردن ویژگی جدید" -Push

# نظارت مداوم (هر 60 ثانیه)
.\auto-commit.ps1 -Interval 60
```

**Linux/Mac (Bash):**
```bash
chmod +x auto-commit.sh
./auto-commit.sh -m "اضافه کردن ویژگی جدید" -p
```

برای اطلاعات بیشتر، فایل [`GIT_AUTO_COMMIT.md`](GIT_AUTO_COMMIT.md) را مطالعه کنید.

## 📚 مستندات API

پس از اجرای اپلیکیشن، می‌توانید از مستندات خودکار استفاده کنید:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

این مستندات شامل:
- لیست کامل endpoints
- پارامترهای ورودی و خروجی
- مثال‌های استفاده
- امکان تست مستقیم API

## 🧪 تست API

می‌توانید از ابزارهای زیر برای تست API استفاده کنید:

1. **Swagger UI**: http://localhost:8000/docs
2. **Postman**: Import کردن collection
3. **curl**: دستورات خط فرمان
4. **httpie**: ابزار مدرن برای HTTP requests

## 📝 مدل داده Todo

```python
{
  "id": int,                    # شناسه یکتا
  "title": str,                 # عنوان وظیفه (اجباری)
  "description": str | null,    # توضیحات (اختیاری)
  "completed": bool,            # وضعیت انجام
  "created_at": datetime,       # تاریخ ایجاد
  "updated_at": datetime        # تاریخ آخرین به‌روزرسانی
}
```

## 🔧 تنظیمات

متغیرهای محیطی قابل تنظیم:

- `DATABASE_URL`: آدرس اتصال به دیتابیس PostgreSQL
  - پیش‌فرض: `postgresql://postgres:postgres@localhost:5432/tododb`

## 📄 مجوز

این پروژه برای استفاده آموزشی ساخته شده است.

## 👤 نویسنده

این پروژه به عنوان تمرین درس مهندسی نرم‌افزار پیاده‌سازی شده است.

---

**نکته**: برای سوالات و مشکلات، لطفاً issue در repository ایجاد کنید.


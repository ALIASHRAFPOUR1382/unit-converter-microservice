from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import todos
import logging

# تنظیم logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ایجاد FastAPI app
app = FastAPI(
    title="To-Do App Backend API",
    description="یک API کامل برای مدیریت لیست وظایف (To-Do List) با قابلیت CRUD",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در production باید محدود شود
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# اتصال routers
app.include_router(todos.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """
    رویداد startup - ایجاد جداول دیتابیس
    """
    logger.info("در حال راه‌اندازی اپلیکیشن...")
    try:
        init_db()
        logger.info("جداول دیتابیس با موفقیت ایجاد شدند")
    except Exception as e:
        logger.error(f"خطا در ایجاد جداول دیتابیس: {e}")


@app.get("/", tags=["health"])
def root():
    """
    صفحه اصلی - اطلاعات API
    """
    return {
        "message": "خوش آمدید به To-Do App Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint برای بررسی وضعیت سرویس
    """
    return {
        "status": "healthy",
        "service": "To-Do App Backend",
        "version": "1.0.0"
    }


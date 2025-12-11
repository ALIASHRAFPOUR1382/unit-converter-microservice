from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import todos
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="To-Do App Backend API",
    description="A complete API for managing To-Do List with CRUD capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todos.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """
    Startup event - Create database tables
    """
    logger.info("Starting application...")
    try:
        init_db()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")


@app.get("/", tags=["health"])
def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "Welcome to To-Do App Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint to verify service status
    """
    return {
        "status": "healthy",
        "service": "To-Do App Backend",
        "version": "1.0.0"
    }


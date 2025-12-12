# To-Do App Backend API

A complete and powerful API for managing To-Do Lists with full CRUD capabilities, pagination, filtering, and sorting.

## 📋 Table of Contents

- [Project Introduction](#project-introduction)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [API Usage](#api-usage)
- [Docker](#docker)
- [Git Workflow](#git-workflow)
- [API Documentation](#api-documentation)
- [Unit Converter](#unit-converter)

## 🎯 Project Introduction

This project is a complete Backend service for managing To-Do Lists, including full CRUD (Create, Read, Update, Delete) operations. This API is built using FastAPI and uses PostgreSQL as the database.

### Main Features

- ✅ Full CRUD operations
- 📄 Pagination for task lists
- 🔍 Filtering by completion status
- 📊 Sorting by creation date
- 🐳 Docker and Docker Compose for easy deployment
- 📚 Automatic API documentation (Swagger UI)
- 🔒 Complete data validation
- ⚡ High performance with FastAPI
- 🔄 Unit converter with graphical interface

## 🛠 Technologies Used

- **FastAPI**: Modern and fast framework for building APIs
- **PostgreSQL/SQLite**: Relational database
- **SQLAlchemy**: ORM for Python
- **Pydantic**: Data validation and serialization
- **Docker & Docker Compose**: Containerization
- **Uvicorn**: ASGI server for FastAPI

## 📁 Project Structure

```
cs_project/
├── .git/
├── .gitignore
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.ps1                 # Windows run script
├── run.sh                  # Linux/Mac run script
├── test_converter.py       # Unit converter test script
├── converter_interactive.py # Interactive converter
├── static/
│   └── converter.html     # Graphical converter interface
└── app/
    ├── __init__.py
    ├── main.py              # FastAPI application
    ├── database.py          # Database connection & session
    ├── models.py            # SQLAlchemy models
    ├── schemas.py           # Pydantic schemas
    ├── crud.py              # CRUD operations
    └── routers/
        ├── __init__.py
        ├── todos.py         # Todo API endpoints
        └── converter.py     # Unit converter endpoints
```

## 🚀 Installation and Setup

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for Docker deployment)
- PostgreSQL (if you want to run without Docker)

### Method 1: Using Docker (Recommended)

1. Clone the project:
```bash
git clone <repository-url>
cd cs_project
```

2. Run with Docker Compose:
```bash
docker-compose up --build
```

This command will:
- Start PostgreSQL
- Build and run the FastAPI application
- Automatically create database tables

3. Access the API:
- API: http://localhost:8000
- Swagger Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc
- Unit Converter: http://localhost:8000/static/converter.html

### Method 2: Local Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Database setup:
   - For SQLite (default, no setup required):
     - The database file (`tododb.db`) will be created automatically
   - For PostgreSQL:
     - Install and start PostgreSQL
     - Create a database named `tododb`
     - Set the environment variable `DATABASE_URL`:
     ```bash
     export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/tododb"
     ```

4. Run the application:
```bash
# Using the run script (Windows)
.\run.ps1

# Using the run script (Linux/Mac)
./run.sh

# Or manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Usage

### Main Endpoints

#### 1. Create a new Todo
```bash
POST /api/todos
Content-Type: application/json

{
  "title": "Learn FastAPI",
  "description": "Study FastAPI documentation",
  "completed": false
}
```

#### 2. Get Todos list
```bash
GET /api/todos?page=1&page_size=10&completed=false
```

Query parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10, maximum: 100)
- `completed`: Filter by status (true/false/null for all)

#### 3. Get a Todo
```bash
GET /api/todos/{id}
```

#### 4. Full update Todo (PUT)
```bash
PUT /api/todos/{id}
Content-Type: application/json

{
  "title": "Learn FastAPI - Updated",
  "description": "Completed",
  "completed": true
}
```

#### 5. Partial update Todo (PATCH)
```bash
PATCH /api/todos/{id}
Content-Type: application/json

{
  "completed": true
}
```

#### 6. Delete Todo
```bash
DELETE /api/todos/{id}
```

#### 7. Health Check
```bash
GET /health
```

### Usage Examples with curl

```bash
# Create a new Todo
curl -X POST "http://localhost:8000/api/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy a book",
    "description": "Buy Python book",
    "completed": false
  }'

# Get Todos list
curl "http://localhost:8000/api/todos?page=1&page_size=10"

# Get a Todo
curl "http://localhost:8000/api/todos/1"

# Update Todo
curl -X PATCH "http://localhost:8000/api/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete Todo
curl -X DELETE "http://localhost:8000/api/todos/1"
```

## 🔄 Unit Converter

The project includes a unit converter feature with both API endpoints and a graphical interface.

### Graphical Interface

Access the converter at: **http://localhost:8000/static/converter.html**

Features:
- Beautiful, user-friendly interface
- Support for length, weight, and temperature conversions
- Real-time conversion using the API

### API Endpoints

#### Convert Units
```bash
POST /api/converter/convert
Content-Type: application/json

{
  "value": 100,
  "from_unit": "kilometer",
  "to_unit": "mile",
  "unit_type": "length"
}
```

#### Get Available Units
```bash
GET /api/converter/units
```

### Supported Units

**Length:**
- meter, kilometer, centimeter, millimeter
- mile, foot, inch, yard

**Weight:**
- kilogram, gram, pound, ounce, ton

**Temperature:**
- celsius, fahrenheit, kelvin

### Standalone Converter Scripts

You can also use the converter without the server:

```bash
# Quick test with examples
python test_converter.py

# Interactive mode
python converter_interactive.py
```

## 🐳 Docker

### Useful Docker Commands

```bash
# Run services
docker-compose up

# Run in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f app

# Rebuild
docker-compose up --build
```

## 🔄 Git Workflow

This project uses Git workflow with feature branches:

### Feature Branches

- `feature/database-setup`: Database layer implementation
- `feature/api-endpoints`: API endpoints implementation
- `feature/docker-setup`: Docker configuration
- `feature/unit-converter`: Unit converter feature

### Pull Requests

Pull Requests are used to merge code into the main branch (`main` or `master`).

### Commits

Commits should be clear and descriptive, showing the gradual progress of the project.

### Incremental Commit System

This project includes an automatic commit system for incremental updates:

#### Quick Usage

**Windows (PowerShell):**
```powershell
# Auto commit with default message
.\auto-commit.ps1

# Commit with custom message and push
.\auto-commit.ps1 -Message "Add new feature" -Push

# Continuous monitoring (every 60 seconds)
.\auto-commit.ps1 -Interval 60
```

**Linux/Mac (Bash):**
```bash
chmod +x auto-commit.sh
./auto-commit.sh -m "Add new feature" -p
```

For more information, see the [`GIT_AUTO_COMMIT.md`](GIT_AUTO_COMMIT.md) file.

## 📚 API Documentation

After running the application, you can use the automatic documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

This documentation includes:
- Complete list of endpoints
- Input and output parameters
- Usage examples
- Direct API testing capability

## 🧪 Testing the API

You can use the following tools to test the API:

1. **Swagger UI**: http://localhost:8000/docs
2. **Postman**: Import collection
3. **curl**: Command line tools
4. **httpie**: Modern tool for HTTP requests
5. **Graphical Interface**: http://localhost:8000/static/converter.html (for unit converter)

## 📝 Todo Data Model

```python
{
  "id": int,                    # Unique identifier
  "title": str,                 # Task title (required)
  "description": str | null,    # Description (optional)
  "completed": bool,            # Completion status
  "created_at": datetime,       # Creation date
  "updated_at": datetime        # Last update date
}
```

## 🔧 Configuration

Configurable environment variables:

- `DATABASE_URL`: Database connection URL
  - Default (SQLite): `sqlite:///./tododb.db`
  - PostgreSQL: `postgresql://postgres:postgres@localhost:5432/tododb`

## 📄 License

This project is created for educational purposes.

## 👤 Author

This project is implemented as an exercise for Software Engineering course.

---

**Note**: For questions and issues, please create an issue in the repository.

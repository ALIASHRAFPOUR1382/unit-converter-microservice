# استفاده از Python 3.11 به عنوان base image
FROM python:3.11-slim

# تنظیم working directory
WORKDIR /app

# نصب system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# کپی requirements.txt
COPY requirements.txt .

# نصب Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# کپی کد اپلیکیشن
COPY ./app /app/app

# Expose port
EXPOSE 8000

# اجرای اپلیکیشن
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


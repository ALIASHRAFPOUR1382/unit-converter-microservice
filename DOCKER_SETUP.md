# Docker Setup Guide

This guide explains how to run the application using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher

## Quick Start

### 1. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This command will:
- Build the FastAPI application image
- Start PostgreSQL database
- Start the FastAPI application
- Create necessary volumes for data persistence

### 2. Access the Application

Once the containers are running, you can access:

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Unit Converter**: http://localhost:8000/static/converter.html
- **Health Check**: http://localhost:8000/health

### 3. Stop the Application

```bash
docker-compose down
```

To also remove volumes (database data will be lost):

```bash
docker-compose down -v
```

## Docker Compose Commands

### View Logs

```bash
# View all logs
docker-compose logs -f

# View app logs only
docker-compose logs -f app

# View database logs only
docker-compose logs -f db
```

### Rebuild After Code Changes

```bash
docker-compose up --build
```

### Run in Background (Detached Mode)

```bash
docker-compose up -d
```

### Stop Services

```bash
docker-compose stop
```

### Restart Services

```bash
docker-compose restart
```

## Docker Volumes

The following volumes are configured:

- `postgres_data`: PostgreSQL database data (persistent)
- `./exports`: Excel export files (mapped to host)
- `./static`: Static files (mapped to host)

## Environment Variables

The application uses the following environment variables:

- `DATABASE_URL`: Database connection string (automatically set in docker-compose.yml)

Default configuration:
- Database: PostgreSQL
- Host: `db` (internal Docker network)
- Port: `5432`
- Database: `tododb`
- User: `postgres`
- Password: `postgres`

## Troubleshooting

### Port Already in Use

If port 8000 or 5432 is already in use, modify the ports in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change host port
```

### Database Connection Issues

1. Ensure the database container is healthy:
   ```bash
   docker-compose ps
   ```

2. Check database logs:
   ```bash
   docker-compose logs db
   ```

3. Wait for database to be ready (health check configured)

### Application Not Starting

1. Check application logs:
   ```bash
   docker-compose logs app
   ```

2. Rebuild the image:
   ```bash
   docker-compose build --no-cache app
   ```

### Static Files Not Loading

Ensure the `static` directory exists and contains `converter.html`:

```bash
ls -la static/
```

## Production Considerations

For production deployment, consider:

1. **Security**:
   - Change default database credentials
   - Use environment variables for sensitive data
   - Restrict CORS origins
   - Use secrets management

2. **Performance**:
   - Use production ASGI server (Gunicorn with Uvicorn workers)
   - Configure database connection pooling
   - Enable caching
   - Use reverse proxy (Nginx)

3. **Monitoring**:
   - Add health check endpoints
   - Configure logging
   - Set up monitoring tools

4. **Backup**:
   - Regular database backups
   - Export file management

## Manual Docker Build

If you prefer to build manually:

```bash
# Build the image
docker build -t todo-app .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/tododb \
  -v $(pwd)/exports:/app/exports \
  -v $(pwd)/static:/app/static \
  todo-app
```

## Clean Up

Remove all containers, networks, and volumes:

```bash
docker-compose down -v --remove-orphans
```

Remove unused images:

```bash
docker image prune -a
```


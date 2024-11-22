#!/bin/sh

echo "Starting entrypoint script..."

# Wait for PostgreSQL to be ready (Optional but recommended)
# You can use a simple loop here to check connectivity
until pg_isready -h pgsql; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done

# Execute init.sql to set up the database schema
echo "Running init.sql..."
psql -h pgsql -U postgres -d lcnc_db_dev -f /app/init.sql

# Create the tables first
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

# Seed the database if applicable
if [ "$LCNC_ENV" = "development" ]; then
    echo "Running database seeders..."
    python /app/seed.py
fi

# Start the FastAPI server
echo "Starting FastAPI server..."
PYTHONPATH=/app uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Start the Celery worker in the background
# echo "Starting Celery worker..."
# PYTHONPATH=/app celery -A tasks.celery worker --loglevel=info 

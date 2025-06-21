# Run migrations
alembic upgrade head

# Start FastAPI app with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000

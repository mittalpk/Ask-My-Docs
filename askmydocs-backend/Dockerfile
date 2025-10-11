FROM python:3.12-slim

# Install system dependencies for asyncpg/PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

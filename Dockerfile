FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if needed (e.g. gcc for some python deps)
# RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Expose port
EXPOSE 8000

# Set default env vars
ENV AZURE_KEYVAULT_URL=""

# Run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Docker deployment for Finsight

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY finsight/ ./finsight/
COPY setup.py .
COPY README.md .

# Install the package
RUN pip install -e .

# Expose the API port
EXPOSE 8000

# Default command (can be overridden)
CMD ["uvicorn", "finsight.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

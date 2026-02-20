# Use slim Python 3.11 image for a smaller, secure footprint
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user for security
RUN groupadd -r django && useradd -r -g django django

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies (clearing cache afterwards)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Change ownership to the non-root user
RUN chown -R django:django /usr/src/app /var/log

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Run server using gunicorn instead of the development runserver
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "hello_world_django_app.wsgi:application"]

FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Reuse the non-root user that already exists in the Playwright base image.
RUN mkdir -p /app /app/shared /app/logs /app/config && \
    chown -R pwuser:pwuser /app

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=pwuser:pwuser app/ app/
COPY --chown=pwuser:pwuser config/ config/
COPY --chown=pwuser:pwuser main.py .

# Switch to non-root user
USER pwuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HOME=/home/pwuser

# Run the application
CMD ["python", "main.py"]

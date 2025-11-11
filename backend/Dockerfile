FROM python:3.11-slim

# Set working directory (NOT /app to avoid conflicts)
WORKDIR /code

# Install system dependencies AND Playwright dependencies as root
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    # Playwright/Chromium dependencies
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (security best practice)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /code

# Set up PATH and cache folder
ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/.cache/ms-playwright

# Copy requirements first (Docker layer caching)
# --chown=user:group (transfer ownership from root to user)
COPY --chown=appuser:appuser requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# RUN pip install --no-cache-dir playwright && \
#     playwright install --with-deps chromium

RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium

# Create playwright cache directory and set permissions
RUN mkdir -p /home/appuser/.cache/ms-playwright && \
    chown -R appuser:appuser /home/appuser/.cache

# NOW switch to non-root user
USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application

# CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
# migration is written as seperate service in compose.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

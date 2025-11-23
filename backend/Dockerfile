FROM python:3.11-slim as builder

WORKDIR /code

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir playwright

# ============================================
# Final stage
# ============================================
FROM python:3.11-slim

WORKDIR /code

# Install ONLY runtime dependencies + Playwright system deps (as root)
RUN apt-get update && apt-get install -y \
    libpq5 \
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
    # Additional dependencies that playwright install --with-deps would install
    libglib2.0-0 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxext6 \
    libxcb-dri3-0 \
    libxshmfence1 \
    fonts-liberation \
    libappindicator3-1 \
    libu2f-udev \
    xdg-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /code

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set up Playwright cache path
ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/.cache/ms-playwright

# Create cache directory with correct permissions
RUN mkdir -p /home/appuser/.cache/ms-playwright && \
    chown -R appuser:appuser /home/appuser/.cache

# Switch to non-root user
# Switch to non-root user
USER appuser

# Skip host validation since we already installed all deps as root
ENV PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true

# Install Chromium browser ONLY (dependencies already installed as root)
RUN playwright install chromium

# Copy application code
COPY --chown=appuser:appuser . .

#   For Railway (Production)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}    

# # For Dev

# EXPOSE 8000

# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


#   ------------------------------ END


# FROM python:3.11-slim

# # Set working directory (NOT /app to avoid conflicts)
# WORKDIR /code

# # Install system dependencies AND Playwright dependencies as root
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     libpq-dev \
#     curl \
#     # Playwright/Chromium dependencies
#     libnss3 \
#     libnspr4 \
#     libatk1.0-0 \
#     libatk-bridge2.0-0 \
#     libcups2 \
#     libdrm2 \
#     libdbus-1-3 \
#     libxkbcommon0 \
#     libxcomposite1 \
#     libxdamage1 \
#     libxfixes3 \
#     libxrandr2 \
#     libgbm1 \
#     libasound2 \
#     libpango-1.0-0 \
#     libcairo2 \
#     && rm -rf /var/lib/apt/lists/*

# # Create non-root user (security best practice)
# RUN useradd -m -u 1000 appuser && \
#     chown -R appuser:appuser /code

# # Set up PATH and cache folder
# ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/.cache/ms-playwright

# # Copy requirements first (Docker layer caching)
# # --chown=user:group (transfer ownership from root to user)
# COPY --chown=appuser:appuser requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# RUN pip install --no-cache-dir playwright && \
#     playwright install --with-deps chromium

# # Create playwright cache directory and set permissions
# RUN mkdir -p /home/appuser/.cache/ms-playwright && \
#     chown -R appuser:appuser /home/appuser/.cache

# # NOW switch to non-root user
# USER appuser

# # Copy application code
# COPY --chown=appuser:appuser . .

# # Expose port
# EXPOSE 8000

# # Health check
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

# # Run application

# # CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
# # migration is written as seperate service in compose.

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

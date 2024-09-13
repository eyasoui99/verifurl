# Use an official Python runtime as a base image
FROM python:3.9

# Set environment variables to ensure that Python outputs everything to the terminal
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies for Playwright and Xvfb (necessary for running Chromium in Docker)
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libgtk-3-0 \
    libxdamage1 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libx11-xcb1 \
    fonts-liberation \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Install Playwright and its dependencies
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN playwright install --with-deps --force

# Expose port 5000 for Flask
EXPOSE 5000

# Start Xvfb and then run the Flask app using Gunicorn
CMD xvfb-run --auto-servernum --server-args='-screen 0 1920x1080x24' gunicorn app:app --bind 0.0.0.0:7860 --timeout 360

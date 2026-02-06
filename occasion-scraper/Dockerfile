ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.11
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    mariadb \
    mariadb-client \
    nginx \
    nodejs \
    npm \
    bash \
    curl \
    git

# Create directories
RUN mkdir -p /app/backend /app/frontend /run/mysqld /var/lib/mysql

# Copy backend from repo root
COPY backend /app/backend
WORKDIR /app/backend

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy create_admin script
COPY backend/create_admin.py /app/backend/create_admin.py

# Copy frontend from repo root
COPY frontend /app/frontend
WORKDIR /app/frontend

# Install Node dependencies and build
RUN npm install && npm run build

# Configure nginx
RUN rm -f /etc/nginx/http.d/default.conf
COPY occasion-scraper/nginx.conf /etc/nginx/http.d/app.conf

# Copy startup script
COPY occasion-scraper/run.sh /run.sh
RUN chmod a+x /run.sh

WORKDIR /app

# Expose port for ingress
EXPOSE 80

CMD [ "/run.sh" ]

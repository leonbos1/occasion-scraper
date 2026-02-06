#!/usr/bin/env bash
set -e

echo "================================================"
echo "  Occasion Scraper - Starting"
echo "================================================"

CONFIG_PATH=/data/options.json

# Read configuration
echo "[INFO] Reading configuration..."
MYSQL_ROOT_PASSWORD=$(python3 -c "import json; print(json.load(open('$CONFIG_PATH'))['mysql_root_password'])")
DB_NAME=$(python3 -c "import json; print(json.load(open('$CONFIG_PATH'))['db_name'])")
DB_USER=$(python3 -c "import json; print(json.load(open('$CONFIG_PATH'))['db_user'])")
DB_PASSWORD=$(python3 -c "import json; print(json.load(open('$CONFIG_PATH'))['db_password'])")
ADMIN_EMAIL=$(python3 -c "import json; print(json.load(open('$CONFIG_PATH'))['admin_email'])")
ADMIN_PASSWORD=$(python3 -c "import json; print(json.load(open('$CONFIG_PATH'))['admin_password'])")

# Initialize MySQL database
echo "[INFO] Initializing MySQL..."
if [ ! -d "/data/mysql/mysql" ]; then
    echo "[INFO] First run - creating database..."
    mysql_install_db --user=root --datadir=/data/mysql
fi

# Start MySQL
echo "[INFO] Starting MySQL..."
mysqld --user=root --datadir=/data/mysql --skip-networking=0 &
MYSQL_PID=$!

# Wait for MySQL to be ready
echo "[INFO] Waiting for MySQL..."
for i in {1..30}; do
    if mysqladmin ping -h localhost --silent 2>/dev/null; then
        echo "[INFO] MySQL is ready!"
        break
    fi
    sleep 1
done

# Create database and user
echo "[INFO] Setting up database..."
mysql -u root <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED BY '$MYSQL_ROOT_PASSWORD';
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
EOF

# Set environment for backend
export MYSQL_HOST=localhost
export MYSQL_DATABASE=$DB_NAME
export MYSQL_USER=$DB_USER
export MYSQL_PASSWORD=$DB_PASSWORD
export ADMIN_EMAIL=$ADMIN_EMAIL
export ADMIN_PASSWORD=$ADMIN_PASSWORD
export FLASK_APP=backend:create_app

# Start Flask backend
echo "[INFO] Starting Flask backend..."
cd /app/backend
python3 -m flask run --host=127.0.0.1 --port=5000 &
FLASK_PID=$!

# Wait for backend
echo "[INFO] Waiting for backend..."
for i in {1..30}; do
    if curl -sf http://127.0.0.1:5000/api/health >/dev/null 2>&1; then
        echo "[INFO] Backend is ready!"
        break
    fi
    sleep 1
done

# Create admin user
echo "[INFO] Creating admin user..."
cd /app/backend
python3 create_admin.py || echo "[WARN] Admin user creation failed"

# Start nginx
echo "[INFO] Starting nginx..."
nginx -g "daemon off;" &
NGINX_PID=$!

echo "================================================"
echo "  Occasion Scraper is running!"
echo "  MySQL PID: $MYSQL_PID"
echo "  Flask PID: $FLASK_PID"
echo "  Nginx PID: $NGINX_PID"
echo "================================================"

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?

#!/bin/bash
# Database Initialization Script for Home Assistant Addon
# This script initializes the MySQL database for first-time setup

set -e

echo "================================================"
echo "  Database Initialization Script"
echo "================================================"

# Read environment variables
MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD}"
MYSQL_DATABASE="${MYSQL_DATABASE}"
MYSQL_USER="${MYSQL_USER}"
MYSQL_PASSWORD="${MYSQL_PASSWORD}"

# Validate required variables
if [ -z "$MYSQL_ROOT_PASSWORD" ] || [ -z "$MYSQL_DATABASE" ] || [ -z "$MYSQL_USER" ] || [ -z "$MYSQL_PASSWORD" ]; then
    echo "ERROR: Required environment variables not set"
    echo "Required: MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD"
    exit 1
fi

echo "Waiting for MySQL to be available..."
until mysqladmin ping -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" --silent &> /dev/null; do
    echo "  MySQL not ready, waiting..."
    sleep 2
done

echo "MySQL is available!"

# Check if database exists
DB_EXISTS=$(mysql -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES LIKE '$MYSQL_DATABASE';" | grep -c "$MYSQL_DATABASE" || true)

if [ "$DB_EXISTS" -eq 0 ]; then
    echo "Creating database: $MYSQL_DATABASE"
    mysql -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
        CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOSQL
    echo "✓ Database created"
else
    echo "✓ Database $MYSQL_DATABASE already exists"
fi

# Check if user exists
USER_EXISTS=$(mysql -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT User FROM mysql.user WHERE User = '$MYSQL_USER';" | grep -c "$MYSQL_USER" || true)

if [ "$USER_EXISTS" -eq 0 ]; then
    echo "Creating user: $MYSQL_USER"
    mysql -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
        CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
        GRANT ALL PRIVILEGES ON \`$MYSQL_DATABASE\`.* TO '$MYSQL_USER'@'%';
        FLUSH PRIVILEGES;
EOSQL
    echo "✓ User created and granted privileges"
else
    echo "✓ User $MYSQL_USER already exists"
    # Update password in case it changed
    echo "  Updating user password..."
    mysql -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
        ALTER USER '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
        GRANT ALL PRIVILEGES ON \`$MYSQL_DATABASE\`.* TO '$MYSQL_USER'@'%';
        FLUSH PRIVILEGES;
EOSQL
    echo "✓ User password updated"
fi

echo "================================================"
echo "  Database initialization complete!"
echo "================================================"
echo "Database: $MYSQL_DATABASE"
echo "User: $MYSQL_USER"
echo "================================================"

exit 0

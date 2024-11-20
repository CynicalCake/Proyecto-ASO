#!/bin/bash

# Uso: ./create_user_db.sh <username> <password> <db_type>

USERNAME=$1
PASSWORD=$2
DB_TYPE=$3
DB_NAME=$4

if [ "$DB_TYPE" = "postgres" ]; then
    # Crear usuario y base de datos en PostgreSQL
    sudo -u postgres psql -c "CREATE USER $USERNAME WITH PASSWORD '$PASSWORD';"
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME  OWNER $USERNAME;"
    sudo -u postgres psql -c "REVOKE ALL ON DATABASE $DB_NAME FROM PUBLIC;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $USERNAME;"
    echo "Usuario y base de datos PostgreSQL creados para $USERNAME"
elif [ "$DB_TYPE" = "mysql" ]; then
    # Crear usuario y base de datos en MySQL
    sudo mysql -e "CREATE USER '$USERNAME'@'localhost' IDENTIFIED BY '$PASSWORD';"
    sudo mysql -e "CREATE DATABASE $DB_NAME;"
    sudo mysql -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$USERNAME'@'localhost';"
    sudo mysql -e "FLUSH PRIVILEGES;"
    echo "Usuario y base de datos MySQL creados para $USERNAME"
else
    echo "Tipo de base de datos no válido. Use 'postgres' o 'mysql'."
    exit 1
fi

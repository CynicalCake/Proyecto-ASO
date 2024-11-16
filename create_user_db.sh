#!/bin/bash

# Uso: ./create_user_db.sh <username> <password> <db_type>

USERNAME=$1
PASSWORD=$2
DB_TYPE=$3

if [ "$DB_TYPE" = "postgres" ]; then
    # Crear usuario y base de datos en PostgreSQL
    sudo -u postgres psql -c "CREATE USER $USERNAME WITH PASSWORD '$PASSWORD';"
    sudo -u postgres psql -c "CREATE DATABASE $USERNAME OWNER $USERNAME;"
    sudo -u postgres psql -c "REVOKE ALL ON DATABASE $USERNAME FROM PUBLIC;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $USERNAME TO $USERNAME;"
    echo "Usuario y base de datos PostgreSQL creados para $USERNAME"
elif [ "$DB_TYPE" = "mysql" ]; then
    # Crear usuario y base de datos en MySQL
    sudo mysql -e "CREATE USER '$USERNAME'@'localhost' IDENTIFIED BY '$PASSWORD';"
    sudo mysql -e "CREATE DATABASE $USERNAME;"
    sudo mysql -e "GRANT ALL PRIVILEGES ON $USERNAME.* TO '$USERNAME'@'localhost';"
    sudo mysql -e "FLUSH PRIVILEGES;"
    echo "Usuario y base de datos MySQL creados para $USERNAME"
else
    echo "Tipo de base de datos no válido. Use 'postgres' o 'mysql'."
    exit 1
fi

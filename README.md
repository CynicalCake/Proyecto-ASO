# Administrador de Hosting Web

Este proyecto es un sistema de administración de hosting web para OpenSUSE, que permite crear y gestionar sitios web con bases de datos MySQL o PostgreSQL.

## Requisitos del Sistema

- OpenSUSE (versión recomendada: 15.2 o superior)
- Python 3.6 o superior
- Acceso root o sudo

## Instalación

### 1. Descomprimir el archivo zip

```bash
unzip administrador-hosting-web.zip
cd administrador-hosting-web
```

### 2. Instalar Dependencias del Sistema

Ejecute el siguiente comando para instalar todas las dependencias necesarias:

```bash
sudo zypper install apache2 mysql mysql-server postgresql postgresql-server vsftpd btrfs-progs php php-mysql php-pgsql phpMyAdmin phpPgAdmin
```

### 3. Configurar Servicios

Habilite e inicie los servicios necesarios:

```bash
sudo systemctl enable --now apache2 mysql postgresql vsftpd
```

### 4. Configurar Base de Datos

Para MySQL:
```bash
sudo mysql_secure_installation
```

Para PostgreSQL:
```bash
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'tu_contraseña';
\\q
```

### 5. Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

### 6. Configurar Permisos

Asegúrese de que el usuario que ejecutará el script tenga permisos sudo sin contraseña para los comandos necesarios. Añada las siguientes líneas a /etc/sudoers usando `visudo`:

```
usuario ALL=(ALL) NOPASSWD: /usr/sbin/useradd, /usr/sbin/userdel, /usr/bin/chpasswd, /usr/bin/btrfs, /usr/bin/tee, /usr/bin/sed, /usr/bin/rm, /usr/sbin/apache2ctl, /usr/sbin/service
```

Además, se debe otorgar manualmente los permisos al archivo `create_user_db.sh`:
```
Clic derecho
Propiedades
Permisos
Otros -> Lectura y escritura posibles
Es ejecutable -> Marcado
```

### 7. Configurar phpMyAdmin y phpPgAdmin

Asegúrese de que phpMyAdmin y phpPgAdmin estén correctamente configurados en Apache. Puede necesitar ajustar los archivos de configuración en /etc/apache2/conf.d/.

## Uso

Para iniciar la aplicación, ejecute:

```bash
python3 interfazGeneral.py
```

## Funcionalidades

- Crear nuevos sitios web con bases de datos MySQL o PostgreSQL
- Asignar cuotas de espacio a los sitios web
- Editar configuraciones de sitios web existentes
- Eliminar sitios web y usuarios asociados

## Notas Importantes

- Este script debe ejecutarse con privilegios de superusuario o con un usuario que tenga los permisos sudo adecuados.
- Asegúrese de tener copias de seguridad antes de realizar operaciones de eliminación o modificación.
- La seguridad del sistema depende de la correcta configuración de los servicios y permisos.

## Solución de Problemas

Si encuentra problemas al acceder a phpMyAdmin o phpPgAdmin a través del proxy, asegúrese de que la configuración de Apache y los archivos .conf de estos servicios estén correctamente configurados.

Para phpMyAdmin, puede ser necesario añadir la siguiente línea en el archivo de configuración (/etc/phpMyAdmin/config.inc.php):

```php
$cfg['PmaAbsoluteUri'] = 'http://www.ejemplo.com/basededatos/';
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abra un issue o realice un pull request con sus sugerencias.

## Licencia

Universidad Mayor de San Simón, Facultad de Ciencias y Tecnología, Carrera de Licenciatura en Ingeniería de Sistemas

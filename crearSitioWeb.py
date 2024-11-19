import subprocess
from eliminarUsuario import eliminarSitioWeb, eliminarHost, eliminarVirtualHost


def agregarURL(sitioWeb):

    try:
        with open('/etc/hosts','r') as f:
            if any(sitioWeb in line for line in f):
                print("URL ya existe")
                return
    except FileNotFoundError:
        print("error URL")
        return

    comando =f'echo "127.0.0.1       www.{sitioWeb}"  | tee -a /etc/hosts'
    try:
        subprocess.run(comando,
                        shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"error al crear URL")
        raise e

def crearDirectorio(sitioWeb):
    subvolume=f'btrfs subvolume create /srv/www/{sitioWeb}'
    ruta =f'mkdir -p /srv/www/{sitioWeb}/public_html'

    try:
        subprocess.run(subvolume, shell=True, check=True)
        subprocess.run(ruta, shell=True, check=True)
        print(f"Creado directorio y subvolume")
    except subprocess.CalledProcessError as e:
        print(f"error Directorio subvolume")
        raise e

def crearVirtualHost(sitioWeb, nombreBD, gestorBD):
    archivo= f'/etc/apache2/vhosts.d/{sitioWeb}.conf'
    gestor=""
    
    if gestorBD=="PostgreSQL":
        gestor="phppgadmin"
    elif gestorBD=="MySQL":
        gestor="phpmyadmin"

    configuracion=f"""
        <VirtualHost *:80>
        ServerName www.{sitioWeb}
        DocumentRoot /srv/www/{sitioWeb}/public_html
        
        <Directory /srv/www/{sitioWeb}/public_html>
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
            Directoryindex index.php
        </Directory>
        
        <Location /{nombreBD}/>                AuthType Basic
                AuthName "Acceso Restringido"
                AUthUserFile /srv/www/{sitioWeb}/.htpasswd
                Require valid-user

                Header set Cache-Control "max-age=0, no-store, must-revalidate"
                Header set Pragma "no-cache"
                Header set EXpires "0"

                ProxyPreserveHost On
                ProxyPass http://localhost/{gestor}/
                ProxyPassReverse  http://localhost/{gestor}/
        </Location>

        ErrorLog /var/log/apache2/{sitioWeb}_error.log
        CustomLog /var/log/apache2/{sitioWeb}_access.log combined
        
    </VirtualHost>
    """

    try:
        with open(archivo,'w') as archivo_abierto:
            archivo_abierto.write(configuracion)
        print(f"archivo creado y escrito")
    except Exception as e:
            print(f"error al crear virtual host")
            raise e

def crearIndex(nombreUser, sitioWeb):
    comando =f'echo "<h1>Bienvenido a {sitioWeb}</h1>" | tee /srv/www/{sitioWeb}/public_html/index.php'
    asignarPro=f'chown {nombreUser}:ftp /srv/www/{sitioWeb}/public_html/index.php'
    asignarPer=f'chmod 755 /srv/www/{sitioWeb}/public_html/index.php'
    try:
        subprocess.run(comando, shell=True, check=True)
        subprocess.run(asignarPro, shell=True, check=True)
        subprocess.run(asignarPer, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"error index.php")
        raise e

def crearUsuario(sitioWeb, nombreUser, contra):
    usuario=f'useradd -d /srv/www/{sitioWeb}/public_html -m {nombreUser}'
    try: 
        subprocess.run(usuario, shell=True, check=True)
        print(f"usuario creado")
        aux=1
    except subprocess.CalledProcessError as e:
        print(f"error al crear usuario")

    if(aux==1):
        asignarContra(nombreUser, contra)

def asignarContra(nombreUser, contra):
        asignarContra=f"echo '{nombreUser}:{contra}' | chpasswd"
        try:
            subprocess.run(asignarContra, shell=True, check=True)
            print(f"contraseña asignada")
        except subprocess.CalledProcessError as e:
            print(f"error al asignar contraseña")
            raise e

def asignarPermisos(nombreUser, sitioWeb):
    permiso=f'chmod 755 /srv/www/{sitioWeb}/public_html '
    grupo=f'chown {nombreUser}:ftp /srv/www/{sitioWeb}/public_html '
    carpeta=f'chown {nombreUser}:ftp /srv/www/{sitioWeb}'
    try:
        subprocess.run(permiso, shell=True, check=True)
        subprocess.run(grupo, shell=True, check=True)
        subprocess.run(carpeta, shell=True, check=True)
        print(f"permiso 755")
    except subprocess.CalledProcessError as e:
        print(f"error al asignar permiso")
        raise e

def idSubvolume(sitioWeb):
    comando=f'btrfs subvolume list /srv/www | grep "/{sitioWeb}"'
    try:
        cId=subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
        textId=cId.stdout.decode()
        id=textId.split()[1]
        return id

    except subprocess.CalledProcessError as e:
        print(f"Error al obtener id de subvolume")
        return None

def asignarQuota(quota, sitioWeb):
    id=idSubvolume(sitioWeb)
    print(id)
    asigQuota=f'btrfs qgroup limit {quota} 0/{id} /srv/www/'

    try:
        subprocess.run(asigQuota, shell=True, check=True)
        print(f"Quota asignada")
    except subprocess.CalledProcessError as e:
        print(f"error al asignar quota")
        raise e

def reiniciarApacheFTP():
    apache=f'service apache2 restart'
    vsftpd=f'service vsftpd restart'
    
    try:
        subprocess.run(apache, shell=True, check=True)
        print(f"Apache reinicio")
        subprocess.run(vsftpd, shell=True, check=True)
        print(f"Vsftpd reinicio")
    except subprocess.CalledProcessError as e:
        print(f"error al reiniciar")
        raise e

def create_user(username, password, gestorBD, db_name):
    if gestorBD=="PostgreSQL":
        db_type="postgres"
    elif gestorBD=="MySQL":
        db_type="mysql"

    try:
        print(username, password, db_type, db_name)
        r=subprocess.run(['sudo', '-S', './create_user_db.sh', username, password, db_type, db_name], check=True)
        print("Se creo BD y user BD",r)
    except subprocess.CalledProcessError as e:
        print("No se pudo crear el usuario y la base de datos", e)
        raise e

def authApache(user, contra, sitioWeb):
    print("Crear auth")
    comando=f'htpasswd -bc /srv/www/{sitioWeb}/.htpasswd {user} {contra}'
    print("consiguoi comando", comando)
    try:
        subprocess.run(comando, shell=True, check=True)
        print("Se cre autentificacion apache")
    except subprocess.CalledProcessError as e:
        print("No se pudo crear el archivo de auth")
        raise e


def crearSitioWeb(sitioWeb, nombreUser, contra, quota, gestorBD, nombreBD, userBD, contraBD):
    
    try:
        agregarURL(sitioWeb)
        crearDirectorio(sitioWeb)
        asignarQuota(quota, sitioWeb)
        crearVirtualHost(sitioWeb, nombreBD, gestorBD)
        crearUsuario(sitioWeb, nombreUser, contra)
        asignarPermisos(nombreUser, sitioWeb)
        crearIndex(nombreUser, sitioWeb)
        create_user(userBD, contraBD, gestorBD, nombreBD)
        authApache(nombreUser, contra, sitioWeb)
        reiniciarApacheFTP()
    except Exception as e:
        eliminarSitioWeb(sitioWeb)
        eliminarHost(sitioWeb)
        raise Exception("Error al crear usuario") from e

def renombrarDir(antSitio, nuevoSitio):
    renombrar=f'btrfs subvolume snapshot /srv/www/{antSitio} /srv/www/{nuevoSitio}'
    
    try:
        subprocess.run(renombrar, shell=True, check=True)
        print(f"Directorio/Subvolume renombrado")
    except subprocess.CalledProcessError as e:
        print(f"error al renombrar")
        raise e

def cambiarDirRaiz(nombreUser, nuevoSitio):
    cambiar=f'usermod -d /srv/www/{nuevoSitio}/public_html {nombreUser}'
    
    try:
        subprocess.run(cambiar, shell=True, check=True)
        print(f"Directorio/Subvolume renombrado")
    except subprocess.CalledProcessError as e:
        print(f"error al renombrar")
        raise e

def editarSitioWeb(antSitio, nuevoSitio, nombreUser):
    try:
        eliminarHost(antSitio)
        renombrarDir(antSitio, nuevoSitio)
        cambiarDirRaiz(nombreUser, nuevoSitio)
        agregarURL(nuevoSitio)
        crearVirtualHost(nuevoSitio)
        eliminarVirtualHost(antSitio)
        asignarPermisos(nombreUser, nuevoSitio)
        eliminarSitioWeb(antSitio)
        reiniciarApacheFTP()
    except Exception as e:
        raise Exception("Error al editar nombre de Sitio") from e






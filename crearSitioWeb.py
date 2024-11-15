import subprocess
from eliminarUsuario import eliminarSitioWeb, eliminarHost


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

def crearVirtualHost(sitioWeb):
    archivo= f'/etc/apache2/vhosts.d/{sitioWeb}.conf'
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

def crearIndex(sitioWeb):
    comando =f'echo "<h1>Bienvenido a {sitioWeb}</h1>" | tee /srv/www/{sitioWeb}/public_html/index.php'

    try:
        subprocess.run(comando, shell=True, check=True)
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
    try:
        subprocess.run(permiso, shell=True, check=True)
        subprocess.run(grupo, shell=True, check=True)
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


def crearSitioWeb(sitioWeb, nombreUser, contra, quota):
    
    try:
        agregarURL(sitioWeb)
        crearDirectorio(sitioWeb)
        asignarQuota(quota, sitioWeb)
        crearVirtualHost(sitioWeb)
        crearIndex(sitioWeb)
        crearUsuario(sitioWeb, nombreUser, contra)
        asignarPermisos(nombreUser, sitioWeb)
        reiniciarApacheFTP()
    except Exception as e:
        eliminarSitioWeb(sitioWeb)
        eliminarHost(sitioWeb)
        raise Exception("Error al crear usuario") from e


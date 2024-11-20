import subprocess
from crearSitioWeb import idSubvolume

def obtenerUsuarioSitio():
    usuarios = []
    try:
        with open("/etc/passwd", "r") as archivo:
            for ln in archivo:
                part = ln.split(":")
                usuario = part[0]
                carpeta = part[5]
                sitio = carpeta[9:-12]
                if carpeta.startswith("/srv/www"):
                    id = idSubvolume(sitio)
                    quota = obtenerQuota(id)
                    gestorBD, nombreBD = obtenerInfoBD(usuario)
                    usuarios.append((usuario, sitio, gestorBD, nombreBD, quota))
        print(usuarios)
    except FileNotFoundError:
        print("Error al obtener usuarios")
    return usuarios

def obtenerQuota(idUsuario):
    datos = f'btrfs qgroup show -pcre /srv | grep "0/{idUsuario}"'
    try:
        obtDatos = subprocess.run(datos, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
        text = obtDatos.stdout.decode()
        rfer = text.split()[1]
        max_rfer = text.split()[3]
        return f"{rfer}/{max_rfer}"
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener quotas")
        return None
    
def obtenerInfoBD(usuario):
    # Intenta obtener información de PostgreSQL
    try:
        cmd = f"sudo -u postgres psql -tAc \"SELECT datname FROM pg_database WHERE datdba = (SELECT usesysid FROM pg_user WHERE usename = '{usuario}')\""
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout:
            return "PostgreSQL", result.stdout.decode().strip()
    except subprocess.CalledProcessError:
        pass

    # Intenta obtener información de MySQL
    try:
        cmd = f"mysql -N -e \"SHOW DATABASES LIKE '{usuario}_%'\""
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout:
            return "MySQL", result.stdout.decode().strip()
    except subprocess.CalledProcessError:
        pass

    return "N/a", "N/a"

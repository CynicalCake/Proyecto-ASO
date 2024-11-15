import subprocess
from crearSitioWeb import idSubvolume

def obtenerUsuarioSitio():

    usuarios=[]
    try:
        with open("/etc/passwd", "r") as archivo:
            for ln in archivo:
                part=ln.split(":")
                usuario=part[0]
                carpeta=part[5]
                sitio=carpeta[9:-12]
                id=idSubvolume(sitio)
                quota=obtenerQuota(id)
                null= "N/a"

                if carpeta.startswith("/srv/www"):
                    usuarios.append((usuario, sitio, null, null, null, quota ))

        print(usuarios)
    except FileNotFoundError:
        print("Error al obtener usuarios")

    return usuarios

def obtenerQuota(idUsuario):
    datos=f'btrfs qgroup show -pcre /srv | grep "0/{idUsuario}"'
    try:
        obtDatos=subprocess.run(datos, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
        text=obtDatos.stdout.decode()
        rfer=text.split()[1]
        max_rfer=text.split()[3]

        #print(rfer + 'quota'+ max_rfer)
        return f"{rfer}/{max_rfer}"
    
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener quotas")
        return None

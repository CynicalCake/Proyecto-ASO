import subprocess

def eliminarCliente(usuario, sitioWeb):
    eliminarUser(usuario)
    eliminarSitioWeb(sitioWeb)
    eliminarHost(sitioWeb)


def eliminarUser(nombreUser):
    
    borrarUsuario =f'userdel {nombreUser}'
    try:
        subprocess.run(borrarUsuario,
                        shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"error al crear URL")


def eliminarSitioWeb(sitioWeb):

    borrarSitio =f'rm -rf /srv/www/{sitioWeb}'
    try:
        subprocess.run(borrarSitio,
                        shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"error al crear URL")

def eliminarHost(sitioWeb):
    
    borrarURL =f"sed -i '/{sitioWeb}/d' /etc/hosts"
    try:
        subprocess.run(borrarURL,
                        shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"error al crear URL")
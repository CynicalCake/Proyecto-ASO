import tkinter
from tkinter import messagebox
from crearSitioWeb import crearSitioWeb

def mostrarRegistro(actualizar):
    ventana=tkinter.Tk()
    ventana.title("Registro nuevo usuario")
    ventana.geometry("400x300")

    txtNombreUser=tkinter.Label(ventana, text="Nombre de Usuario FTP")
    txtNombreUser.pack()
    nombreUser=tkinter.Entry(ventana)
    nombreUser.pack()

    txtContra=tkinter.Label(ventana, text="Contraseña de Usuario FTP")
    txtContra.pack()
    contra=tkinter.Entry(ventana)
    contra.pack()

    txtSitioWeb=tkinter.Label(ventana, text="Nombre del Sitio Web + Dominio")
    txtSitioWeb.pack()
    sitioWeb=tkinter.Entry(ventana)
    sitioWeb.pack()

    txtQuota=tkinter.Label(ventana, text="Quota")
    txtQuota.pack()
    quota=tkinter.Entry(ventana)
    quota.pack()

    btnRegistro=tkinter.Button(ventana, text="Registrar", command = lambda: (llamarCrearWeb(sitioWeb.get(),
                            nombreUser.get(), contra.get(), quota.get(), ventana), actualizar() ))
    btnRegistro.pack()

    ventana.mainloop()

def llamarCrearWeb(sitioWeb, nombreUser, contra, quota, ventana):

    try:
        crearSitioWeb(sitioWeb, nombreUser, contra, quota)
        messagebox.showinfo("EXITO", "Usuario creado")
        ventana.destroy()

    except Exception as e:
        messagebox.showerror("ERROR", "Error al crear usuario")


if __name__ == "__main__":
    mostrarRegistro()

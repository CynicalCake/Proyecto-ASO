import tkinter
from tkinter import messagebox
from tkinter import ttk
from crearSitioWeb import crearSitioWeb

def mostrarRegistro(actualizar):
    ventana=tkinter.Tk()
    ventana.title("Registro nuevo usuario")
    ventana.geometry("350x470")

    txtNombreUser=tkinter.Label(ventana, text="Nombre de Usuario FTP")
    txtNombreUser.pack()
    nombreUser=tkinter.Entry(ventana)
    nombreUser.pack()

    txtContra=tkinter.Label(ventana, text="Contraseña de Usuario FTP")
    txtContra.pack()
    contra=tkinter.Entry(ventana)
    contra.pack()

    txtSitioWeb=tkinter.Label(ventana, text="Nombre del Sitio Web + Dominio")
    txtSitioWeb.pack(pady=(10, 0))
    txtEjemSw=tkinter.Label(ventana, text="Ejemplo:  taxi.bo", font=("Arial", 8, "italic"))
    txtEjemSw.pack()
    sitioWeb=tkinter.Entry(ventana)
    sitioWeb.pack()

    txtgestorBD=tkinter.Label(ventana, text="Gestor de Base de Datos")
    txtgestorBD.pack()
    opciones=["PostgreSQL", "MySQL"]
    gestorBD=ttk.Combobox(ventana, values=opciones)
    gestorBD.pack()

    txtUserBD=tkinter.Label(ventana, text="Nombre del Usuario BD")
    txtUserBD.pack(pady=(10, 0))
    userBD=tkinter.Entry(ventana)
    userBD.pack()

    txtContraBD=tkinter.Label(ventana, text="Contraseña de Usuario BD")
    txtContraBD.pack()
    contraBD=tkinter.Entry(ventana)
    contraBD.pack()

    txtNombreBD=tkinter.Label(ventana, text="Nombre de BD")
    txtNombreBD.pack()
    nombreBD=tkinter.Entry(ventana)
    nombreBD.pack()

    txtQuota=tkinter.Label(ventana, text="Quota")
    txtQuota.pack()
    txtEjemQ=tkinter.Label(ventana, text="Ejemplo:  1G  ,  500M", font=("Arial", 8, "italic"))
    txtEjemQ.pack()
    quota=tkinter.Entry(ventana)
    quota.pack()
    txtIndQ=tkinter.Label(ventana, text="G: Gigabytes     M:Megabytes     K:Kilobytes", font=("Arial", 8, "italic"))
    txtIndQ.pack()

    btnRegistro=tkinter.Button(ventana, text="Registrar", command = lambda: (llamarCrearWeb(sitioWeb.get(),
                            nombreUser.get(), contra.get(), quota.get(), gestorBD.get(),
                            nombreBD.get(), userBD.get(), contraBD.get(), ventana), actualizar() ))
    btnRegistro.pack(pady=10)

    ventana.mainloop()

def llamarCrearWeb(sitioWeb, nombreUser, contra, quota, gestorBD, nombreBD, userBD, contraBD, ventana):

    if not sitioWeb or not nombreUser or not contra or not quota or not gestorBD or not nombreBD or not userBD or not contraBD:
        messagebox.showwarning("ADVERTENCIA", "Todos los campos deben estar llenos", parent=ventana)
    else:
        try:
            crearSitioWeb(sitioWeb, nombreUser, contra, quota, gestorBD, nombreBD, userBD, contraBD)
            messagebox.showinfo("EXITO", "Usuario creado", parent=ventana)
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("ERROR", "Error al crear usuario",parent=ventana)


if __name__ == "__main__":
    mostrarRegistro()

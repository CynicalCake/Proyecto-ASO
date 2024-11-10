import tkinter
from crearSitioWeb import crearSitioWeb

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

btnRegistro=tkinter.Button(ventana, text="Registrar", command = lambda: crearSitioWeb(sitioWeb.get(),
                            nombreUser.get(), contra.get(), quota.get()))
btnRegistro.pack()

ventana.mainloop()

import tkinter
from tkinter import messagebox, simpledialog
from crearSitioWeb import editarSitioWeb, asignarQuota, asignarContra, reiniciarApacheFTP

def mostrarEditar(ventanaP, usuario, sitioWeb, quota, actualizar):
    ventana=tkinter.Toplevel(ventanaP)
    ventana.title("Editar")
    ventana.geometry("350x240")

    txtSitioWeb=tkinter.Label(ventana, text="Nombre del Sitio Web + Dominio")
    txtSitioWeb.pack(pady=(10,0))
    txtAntSw=tkinter.Label(ventana, text="Nombre actual: "+sitioWeb, font=("Arial", 8, "italic"))
    txtAntSw.pack()
    nsitioWeb=tkinter.Entry(ventana)
    nsitioWeb.pack()

    txtQuota=tkinter.Label(ventana, text="Quota")
    txtQuota.pack()
    nquota=tkinter.Entry(ventana)
    txtAntQuota=tkinter.Label(ventana, text="Quota actual: "+quota, font=("Arial", 8, "italic"))
    txtAntQuota.pack()
    nquota.pack()

    btnCambiarContra=tkinter.Button(ventana, text="Cambiar contraseña", 
                                    command = lambda: (cambiarContra(usuario), actualizar()))
    btnCambiarContra.pack(pady=8)

    btnRegistro=tkinter.Button(ventana, text="Editar", command = lambda: (llamarEditar(sitioWeb,
                            nsitioWeb.get(), usuario, quota, nquota.get(), ventana), actualizar()))
    btnRegistro.pack(pady=(10, 10))

    ventana.mainloop()

def llamarEditar(antSitio, nuevoSitio, nombreUser, antQuota, nuevaQuota, ventana):

    try:
        if not nuevoSitio and not nuevaQuota:
            messagebox.showinfo("No se realizo ediciones", "Ningun campo fue llenado", parent=ventana)

        elif not nuevaQuota and nuevoSitio:
            editarSitioWeb(antSitio, nuevoSitio, nombreUser)
            messagebox.showinfo("EXITO", "nombre de Sitio Web editado", parent=ventana)
        elif not nuevoSitio and nuevaQuota:
            asignarQuota(nuevaQuota, antSitio)
            messagebox.showinfo("EXITO", "Quota editada", parent=ventana)
        else : 
            editarSitioWeb(antSitio, nuevoSitio, nombreUser)
            asignarQuota(nuevaQuota, nuevoSitio)
            messagebox.showinfo("EXITO", "nombre de Sitio Web y Quota editado", parent=ventana)

        reiniciarApacheFTP()
        ventana.destroy()

    except Exception as e:
        messagebox.showerror("ERROR", "Error al editar", parent=ventana)

def cambiarContra(nombreUser):

    nuevaContra=simpledialog.askstring("Cambiar contraseña", "Ingresa nueva contraseña")
    if nuevaContra is None:
        print("Nueva contraseña cancelada")
    elif nuevaContra=="":
        messagebox.showwarning("advertencia", "No se ingreso nueva contraseña")
    else:
        try:
            asignarContra(nombreUser, nuevaContra)
            reiniciarApacheFTP()
            messagebox.showinfo("EXITO", "Nueva contraseña asignada")

        except Exception as e:
             messagebox.showerror("ERROR", "No se pudo cambiar contraseña")
            


if __name__ == "__main__":
    mostrarEditar()

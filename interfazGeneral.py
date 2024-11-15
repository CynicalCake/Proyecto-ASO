import tkinter
from tkinter import ttk
from tkinter import messagebox
from obtenerDatos import obtenerUsuarioSitio
from interfazRegistro import mostrarRegistro
from eliminarUsuario import eliminarCliente

def mostrarInterfaz():
    ventana=tkinter.Tk()
    ventana.title("Administrador de Hosting Web")
    ventana.geometry("1000x700")

    txtTitulo=tkinter.Label(ventana, text="Administrador de Hosting Web")
    txtTitulo.pack()

    btnAgregar=tkinter.Button(ventana, text="Agregar usuario", command= lambda: mostrarRegistro(lambda: llenarTabla(tabla)))
    btnAgregar.pack()

    tabla=ttk.Treeview(ventana, columns=("1", "2", "3", "4", "5","6"), show="headings")
    tabla.heading("1", text="Usuario")
    tabla.heading("2", text="Sitioweb")
    tabla.heading("3", text="Gestor de BD")
    tabla.heading("4", text="Nombre BD")
    tabla.heading("5", text="Usuario BD")
    tabla.heading("6", text="Quota")

    tabla.column("1", width=160)
    tabla.column("2", width=160)
    tabla.column("3", width=160)
    tabla.column("4", width=160)
    tabla.column("5", width=160)
    tabla.column("6", width=160)

    llenarTabla(tabla)

    btnEliminar=tkinter.Button(ventana, text="Eliminar usuario", command= lambda: eliminarUsuario(tabla))
    btnEliminar.pack()

    tabla.pack(expand=True, fill="both")

    ventana.mainloop()

def llenarTabla(tabla):

    for i in tabla.get_children():
        tabla.delete(i)

    datosUsers =obtenerUsuarioSitio()
    for usuario, sitio, null, null, null, quota in datosUsers:
        tabla.insert("", "end", values=(usuario, sitio, null, null, null, quota))

def eliminarUsuario(tabla):
    print("en construccion")
    seleccion=tabla.selection()
    item=tabla.item(seleccion)


    if not seleccion:
        messagebox.showwarning("UPPS!", "Tienes que seleccionar un usuario para eliminarlo")
        return

    usuario=item['values'][0]
    sitioWeb=item['values'][1]

    resp=messagebox.askyesno("Eliminr usuario", "¿Estas seguro de eliminar a " + usuario)

    if not resp:
        return
    
    eliminarCliente(usuario, sitioWeb)
    llenarTabla(tabla)


#if __name__ == "__main__":
mostrarInterfaz()

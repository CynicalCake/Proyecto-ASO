import tkinter as tk
from tkinter import messagebox, ttk
import subprocess

def create_user():
    username = username_entry.get()
    password = password_entry.get()
    db_type = db_type_var.get()
    
    try:
        subprocess.run(['sudo', '-S', './create_user_db.sh', username, password, db_type], input=sudo_password.get().encode(), check=True)
        messagebox.showinfo("Éxito", f"Usuario y base de datos {db_type} creados para {username}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "No se pudo crear el usuario y la base de datos")

# Crear ventana principal
root = tk.Tk()
root.title("Administrador de Hosting")

# Crear y colocar widgets
tk.Label(root, text="Nombre de usuario:").grid(row=0, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

tk.Label(root, text="Contraseña:").grid(row=1, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

tk.Label(root, text="Tipo de base de datos:").grid(row=2, column=0)
db_type_var = tk.StringVar(value="postgres")
db_type_combo = ttk.Combobox(root, textvariable=db_type_var, values=["postgres", "mysql"])
db_type_combo.grid(row=2, column=1)

tk.Label(root, text="Contraseña sudo:").grid(row=3, column=0)
sudo_password = tk.Entry(root, show="*")
sudo_password.grid(row=3, column=1)

create_button = tk.Button(root, text="Crear Usuario y BD", command=create_user)
create_button.grid(row=4, column=0, columnspan=2)

root.mainloop()

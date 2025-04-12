import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def mostrar_ventana_clientes():
    ventana = tk.Toplevel()
    ventana.title("Catálogo de Clientes")
    ventana.geometry("900x500")

    # Conexión a la base de datos
    def conectar():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Asegúrate de poner tu contraseña si la tienes
            database="ElRodeo"
        )

    # Función para limpiar campos
    def limpiar():
        entry_telefono.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_rfc.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        entry_clave.delete(0, tk.END)

    # Insertar cliente
    def insertar():
        telefono = entry_telefono.get()
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        rfc = entry_rfc.get()
        correo = entry_correo.get()
        clave = entry_clave.get()

        if nombre == "" or telefono == "" or clave == "":
            messagebox.showwarning("Advertencia", "Los campos nombre, teléfono y clave son obligatorios.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO Clientes (telefono, nombre, direccion, rfc, correo, clave) VALUES (%s, %s, %s, %s, %s, %s)", 
                          (telefono, nombre, direccion, rfc, correo, clave))
            conexion.commit()
            mostrar()
            limpiar()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el cliente: {e}")
        finally:
            conexion.close()

    # Mostrar clientes
    def mostrar():
        for row in tree.get_children():
            tree.delete(row)
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT telefono, nombre, direccion, rfc, correo
            FROM Clientes
            WHERE activo = 1
        """)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conexion.close()

    # Seleccionar un cliente
    def seleccionar(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], 'values')
            entry_telefono.delete(0, tk.END)
            entry_telefono.insert(0, valores[0])
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, valores[1])
            entry_direccion.delete(0, tk.END)
            entry_direccion.insert(0, valores[2])
            entry_rfc.delete(0, tk.END)
            entry_rfc.insert(0, valores[3])
            entry_correo.delete(0, tk.END)
            entry_correo.insert(0, valores[4])

    # Actualizar cliente
    def actualizar():
        telefono = entry_telefono.get()
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        rfc = entry_rfc.get()
        correo = entry_correo.get()
        clave = entry_clave.get()

        if telefono == "":
            messagebox.showwarning("Advertencia", "Seleccione un cliente.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE Clientes
                SET nombre=%s, direccion=%s, rfc=%s, correo=%s, clave=%s
                WHERE telefono=%s
            """, (nombre, direccion, rfc, correo, clave, telefono))
            conexion.commit()
            mostrar()
            limpiar()
            messagebox.showinfo("Éxito", "Cliente actualizado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")
        finally:
            conexion.close()

    # Eliminar cliente
    def eliminar():
        telefono = entry_telefono.get()
        if telefono == "":
            messagebox.showwarning("Advertencia", "Seleccione un cliente.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Deseas eliminar este cliente?")
        if confirm:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM Clientes WHERE telefono=%s", (telefono,))
                conexion.commit()
                mostrar()
                limpiar()
                messagebox.showinfo("Éxito", "Cliente eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")
            finally:
                conexion.close()

    # Etiquetas y campos
    tk.Label(ventana, text="Teléfono").grid(row=0, column=0)
    entry_telefono = tk.Entry(ventana)
    entry_telefono.grid(row=0, column=1)
    entry_telefono.config(state="readonly")

    tk.Label(ventana, text="Nombre").grid(row=1, column=0)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=1, column=1)

    tk.Label(ventana, text="Dirección").grid(row=2, column=0)
    entry_direccion = tk.Entry(ventana)
    entry_direccion.grid(row=2, column=1)

    tk.Label(ventana, text="RFC").grid(row=3, column=0)
    entry_rfc = tk.Entry(ventana)
    entry_rfc.grid(row=3, column=1)

    tk.Label(ventana, text="Correo").grid(row=4, column=0)
    entry_correo = tk.Entry(ventana)
    entry_correo.grid(row=4, column=1)

    tk.Label(ventana, text="Clave").grid(row=5, column=0)
    entry_clave = tk.Entry(ventana)
    entry_clave.grid(row=5, column=1)

    # Botones
    tk.Button(ventana, text="Agregar", command=insertar).grid(row=6, column=0)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=6, column=1)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=6, column=2)
    tk.Button(ventana, text="Limpiar", command=limpiar).grid(row=6, column=3)

    # Tabla
    columnas = ("Teléfono", "Nombre", "Dirección", "RFC", "Correo")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=7, column=0, columnspan=4, pady=10)
    tree.bind("<<TreeviewSelect>>", seleccionar)

    # Mostrar clientes
    mostrar()

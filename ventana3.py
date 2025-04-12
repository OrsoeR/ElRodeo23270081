import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def mostrar_ventana_articulos():
    ventana = tk.Toplevel()
    ventana.title("Catálogo de Artículos")
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
        entry_codigo.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_costo.delete(0, tk.END)
        entry_existencia.delete(0, tk.END)
        combo_categoria.set('')
        combo_unidad.set('')

    # Insertar artículo
    def insertar():
        codigo = entry_codigo.get()
        nombre = entry_nombre.get()
        precio = entry_precio.get()
        costo = entry_costo.get()
        existencia = entry_existencia.get()
        id_categoria = combo_categoria.get().split(" - ")[0]
        id_unidad = combo_unidad.get().split(" - ")[0]

        if nombre == "" or precio == "" or costo == "" or existencia == "":
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO Articulos (codigo, nombre, precio, costo, existencia, unidad_id, categoria_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                          (codigo, nombre, precio, costo, existencia, id_unidad, id_categoria))
            conexion.commit()
            mostrar()
            limpiar()
            messagebox.showinfo("Éxito", "Artículo agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")
        finally:
            conexion.close()

    # Mostrar artículos
    def mostrar():
        for row in tree.get_children():
            tree.delete(row)
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT a.codigo, a.nombre, a.precio, a.costo, a.existencia, c.nombre, u.nombre
            FROM Articulos a
            JOIN Categoria c ON a.categoria_id = c.idcategoria
            JOIN Unidades u ON a.unidad_id = u.idunidad
            WHERE a.activo = 1
        """)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conexion.close()

    # Seleccionar un artículo
    def seleccionar(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], 'values')
            entry_codigo.delete(0, tk.END)
            entry_codigo.insert(0, valores[0])
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, valores[1])
            entry_precio.delete(0, tk.END)
            entry_precio.insert(0, valores[2])
            entry_costo.delete(0, tk.END)
            entry_costo.insert(0, valores[3])
            entry_existencia.delete(0, tk.END)
            entry_existencia.insert(0, valores[4])
            combo_categoria.set(valores[5])
            combo_unidad.set(valores[6])

    # Actualizar artículo
    def actualizar():
        codigo = entry_codigo.get()
        nombre = entry_nombre.get()
        precio = entry_precio.get()
        costo = entry_costo.get()
        existencia = entry_existencia.get()
        id_categoria = combo_categoria.get().split(" - ")[0]
        id_unidad = combo_unidad.get().split(" - ")[0]

        if codigo == "":
            messagebox.showwarning("Advertencia", "Seleccione un artículo.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE Articulos
                SET nombre=%s, precio=%s, costo=%s, existencia=%s, unidad_id=%s, categoria_id=%s
                WHERE codigo=%s
            """, (nombre, precio, costo, existencia, id_unidad, id_categoria, codigo))
            conexion.commit()
            mostrar()
            limpiar()
            messagebox.showinfo("Éxito", "Artículo actualizado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
        finally:
            conexion.close()

    # Eliminar artículo
    def eliminar():
        codigo = entry_codigo.get()
        if codigo == "":
            messagebox.showwarning("Advertencia", "Seleccione un artículo.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Deseas eliminar este artículo?")
        if confirm:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM Articulos WHERE codigo=%s", (codigo,))
                conexion.commit()
                mostrar()
                limpiar()
                messagebox.showinfo("Éxito", "Artículo eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            finally:
                conexion.close()

    # Etiquetas y campos
    tk.Label(ventana, text="Código").grid(row=0, column=0)
    entry_codigo = tk.Entry(ventana)
    entry_codigo.grid(row=0, column=1)
    entry_codigo.config(state="readonly")

    tk.Label(ventana, text="Nombre").grid(row=1, column=0)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=1, column=1)

    tk.Label(ventana, text="Precio").grid(row=2, column=0)
    entry_precio = tk.Entry(ventana)
    entry_precio.grid(row=2, column=1)

    tk.Label(ventana, text="Costo").grid(row=3, column=0)
    entry_costo = tk.Entry(ventana)
    entry_costo.grid(row=3, column=1)

    tk.Label(ventana, text="Existencia").grid(row=4, column=0)
    entry_existencia = tk.Entry(ventana)
    entry_existencia.grid(row=4, column=1)

    tk.Label(ventana, text="Categoría").grid(row=5, column=0)
    combo_categoria = ttk.Combobox(ventana, state="readonly")
    combo_categoria.grid(row=5, column=1)

    tk.Label(ventana, text="Unidad").grid(row=6, column=0)
    combo_unidad = ttk.Combobox(ventana, state="readonly")
    combo_unidad.grid(row=6, column=1)

    # Botones
    tk.Button(ventana, text="Agregar", command=insertar).grid(row=7, column=0)
    tk.Button(ventana, text="Actualizar", command=actualizar).grid(row=7, column=1)
    tk.Button(ventana, text="Eliminar", command=eliminar).grid(row=7, column=2)
    tk.Button(ventana, text="Limpiar", command=limpiar).grid(row=7, column=3)

    # Tabla
    columnas = ("Código", "Nombre", "Precio", "Costo", "Existencia", "Categoría", "Unidad")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=8, column=0, columnspan=4, pady=10)
    tree.bind("<<TreeviewSelect>>", seleccionar)

    # Cargar combos
    def cargar_combos():
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT idcategoria, nombre FROM Categoria")
        categorias = cursor.fetchall()
        combo_categoria['values'] = [f"{c[0]} - {c[1]}" for c in categorias]

        cursor.execute("SELECT idunidad, nombre FROM Unidades")
        unidades = cursor.fetchall()
        combo_unidad['values'] = [f"{u[0]} - {u[1]}" for u in unidades]
        conexion.close()

    cargar_combos()
    mostrar()

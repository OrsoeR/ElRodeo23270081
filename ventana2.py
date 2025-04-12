import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.constants import END
import conexion

class VentanaCategorias:
    def __init__(self, master):
        self.master = master
        self.master.title("🎩 Gestión de Categorías - El Rodeo")
        self.master.geometry("800x600")
        self.master.configure(bg="#f4e2d8")
        self.master.resizable(True, True)

        self.estilo = {
            "bg_frame": "#f4e2d8",
            "bg_marco": "#5e8b3c",
            "color_fuente": "#2e4b1f",
            "fuente_titulo": ("Georgia", 18, "bold"),
            "fuente_texto": ("Georgia", 12),
            "color_botones": "#2d52a0",
            "color_botones_activo": "#13458b"
        }

        self.crear_widgets()
        self.cargar_categorias()

    def crear_widgets(self):
        tk.Label(self.master, text="Gestión de Categorías", bg=self.estilo["bg_frame"], fg=self.estilo["color_fuente"], font=self.estilo["fuente_titulo"]).pack(pady=10)
        main_frame = tk.Frame(self.master, bg=self.estilo["bg_frame"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        search_frame = tk.Frame(main_frame, bg=self.estilo["bg_frame"])
        search_frame.pack(fill="x", pady=5)
        tk.Label(search_frame, text="Buscar:", bg=self.estilo["bg_frame"], fg=self.estilo["color_fuente"], font=self.estilo["fuente_texto"]).pack(side="left")
        self.entry_busqueda = tk.Entry(search_frame, font=self.estilo["fuente_texto"], width=40)
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_categoria)

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Nombre"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("Nombre", width=200, anchor="w")
        scroll = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        form_frame = tk.Frame(main_frame, bg=self.estilo["bg_marco"], bd=3, relief="ridge", padx=10, pady=10)
        form_frame.pack(fill="x", pady=10)
        tk.Label(form_frame, text="ID Categoría:", bg=self.estilo["bg_marco"], fg="white", font=self.estilo["fuente_texto"]).grid(row=0, column=0, sticky="e", pady=5)
        self.entry_id = tk.Entry(form_frame, font=self.estilo["fuente_texto"], state="readonly", width=10)
        self.entry_id.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        tk.Label(form_frame, text="Nombre:", bg=self.estilo["bg_marco"], fg="white", font=self.estilo["fuente_texto"]).grid(row=1, column=0, sticky="e", pady=5)
        self.entry_nombre = tk.Entry(form_frame, font=self.estilo["fuente_texto"], width=30)
        self.entry_nombre.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        button_frame = tk.Frame(self.master, bg=self.estilo["bg_frame"])
        button_frame.pack(pady=10)
        estilo_btn = {
            "bg": self.estilo["color_botones"],
            "fg": "white",
            "font": self.estilo["fuente_texto"],
            "width": 12,
            "relief": "raised",
            "activebackground": self.estilo["color_botones_activo"]
        }
        tk.Button(button_frame, text="Agregar", command=self.agregar_categoria, **estilo_btn).pack(side="left", padx=10)
        tk.Button(button_frame, text="Actualizar", command=self.actualizar_categoria, **estilo_btn).pack(side="left", padx=10)
        tk.Button(button_frame, text="Eliminar", command=self.eliminar_categoria, **estilo_btn).pack(side="left", padx=10)
        tk.Button(button_frame, text="Limpiar", command=self.limpiar_campos, **estilo_btn).pack(side="left", padx=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_categoria)

    def cargar_categorias(self):
        try:
            conn = conexion.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT idcategoria, nombre FROM Categoria ORDER BY nombre")
            categorias = cursor.fetchall()
            for item in self.tree.get_children():
                self.tree.delete(item)
            for categoria in categorias:
                self.tree.insert("", "end", values=categoria)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar categorías:\n{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def seleccionar_categoria(self, event):
        seleccionado = self.tree.focus()
        if seleccionado:
            valores = self.tree.item(seleccionado, "values")
            self.limpiar_campos()
            self.entry_id.config(state="normal")
            self.entry_id.delete(0, END)
            self.entry_id.insert(0, valores[0])
            self.entry_id.config(state="readonly")
            self.entry_nombre.insert(0, valores[1])

    def limpiar_campos(self):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, END)
        self.entry_id.config(state="readonly")
        self.entry_nombre.delete(0, END)
        self.tree.selection_remove(self.tree.selection())

    def validar_campos(self):
        if not self.entry_nombre.get().strip():
            messagebox.showwarning("Validación", "El nombre de la categoría es obligatorio")
            self.entry_nombre.focus_set()
            return False
        return True

    def agregar_categoria(self):
        if not self.validar_campos():
            return
        try:
            conn = conexion.conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Categoria (nombre) VALUES (%s)", (self.entry_nombre.get().strip(),))
            conn.commit()
            messagebox.showinfo("Éxito", "Categoría agregada correctamente")
            self.limpiar_campos()
            self.cargar_categorias()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar categoría:\n{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def actualizar_categoria(self):
        if not self.entry_id.get():
            messagebox.showwarning("Advertencia", "Seleccione una categoría para actualizar")
            return
        if not self.validar_campos():
            return
        try:
            conn = conexion.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE Categoria SET nombre = %s WHERE idcategoria = %s", (self.entry_nombre.get().strip(), self.entry_id.get()))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente")
                self.cargar_categorias()
            else:
                messagebox.showwarning("Advertencia", "No se encontró la categoría")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar categoría:\n{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def eliminar_categoria(self):
        if not self.entry_id.get():
            messagebox.showwarning("Advertencia", "Seleccione una categoría para eliminar")
            return
        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta categoría?\nEsta acción no se puede deshacer.")
        if not confirmacion:
            return
        try:
            conn = conexion.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Categoria WHERE idcategoria = %s", (self.entry_id.get(),))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
                self.limpiar_campos()
                self.cargar_categorias()
            else:
                messagebox.showwarning("Advertencia", "No se encontró la categoría")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar categoría:\n{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def buscar_categoria(self, event=None):
        texto = self.entry_busqueda.get().lower()
        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            if texto in " ".join(map(str, valores)).lower():
                self.tree.selection_set(item)
                self.tree.focus(item)
                break

def mostrar_ventana_categorias():
    root = tk.Tk()
    app = VentanaCategorias(root)
    root.mainloop()

if __name__ == "__main__":
    mostrar_ventana_categorias()

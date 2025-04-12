import tkinter as tk
from tkinter import ttk, messagebox 
from PIL import Image, ImageTk
import os
from ventana1 import mostrar_ventana_clientes
from ventana2 import mostrar_ventana_categorias
from ventana3 import mostrar_ventana_articulos

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.configurar_ventana()
        self.crear_widgets()
        
    def configurar_ventana(self):
        self.root.title("Sistema de Gestión - El Rodeo Charros")
        self.root.geometry("800x600")
        self.root.configure(bg='#8B0000')
        
    def crear_widgets(self):
        main_frame = tk.Frame(self.root, bg='#8B0000')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        try:
            img = Image.open("charro.png") if os.path.exists("charro.png") else None
            if img:
                img = img.resize((180, 180), Image.LANCZOS)
                self.logo = ImageTk.PhotoImage(img)
                tk.Label(main_frame, image=self.logo, bg='#8B0000').pack(pady=10)
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudo cargar la imagen: {e}")
        
        tk.Label(
            main_frame, 
            text="El Rodeo Charros", 
            font=("Helvetica", 24, "bold"), 
            fg='gold', 
            bg='#8B0000'
        ).pack(pady=10)
        
        tk.Label(
            main_frame, 
            text="Sistema de Gestión Integral", 
            font=("Helvetica", 16), 
            fg='white', 
            bg='#8B0000'
        ).pack(pady=5)
        
        self.crear_botones(main_frame)
        
        tk.Label(
            main_frame, 
            text="© 2023 El Rodeo Charros - Tienda de Charretería Tradicional",
            font=("Helvetica", 10),
            fg='white',
            bg='#8B0000'
        ).pack(side='bottom', pady=10)
    
    def crear_botones(self, parent):
        button_frame = tk.Frame(parent, bg='#8B0000')
        button_frame.pack(pady=20)
        
        estilo_btn = {
            'font': ('Helvetica', 12),
            'width': 25,
            'height': 2,
            'bg': '#D4AF37',
            'fg': 'black',
            'activebackground': '#F1C40F',
            'relief': tk.RAISED,
            'borderwidth': 3
        }
        
        tk.Button(
            button_frame, 
            text="🐎 Catálogo de Clientes", 
            command=mostrar_ventana_clientes, 
            **estilo_btn
        ).grid(row=0, column=0, padx=15, pady=10)
        
        tk.Button(
            button_frame, 
            text="🎩 Catálogo de Categorías", 
            command=mostrar_ventana_categorias, 
            **estilo_btn
        ).grid(row=0, column=1, padx=15, pady=10)
        
        tk.Button(
            button_frame, 
            text="🛍️ Catálogo de Artículos", 
            command=mostrar_ventana_articulos, 
            **estilo_btn
        ).grid(row=1, column=0, padx=15, pady=10)
        
        tk.Button(
            button_frame, 
            text="📊 Reportes", 
            command=self.mostrar_reportes, 
            **estilo_btn
        ).grid(row=1, column=1, padx=15, pady=10)
        
        tk.Button(
            button_frame, 
            text="🚪 Salir del Sistema", 
            command=self.root.quit, 
            **estilo_btn
        ).grid(row=2, column=0, columnspan=2, pady=20)
    
    def mostrar_reportes(self):
        messagebox.showinfo("Reportes", "Módulo de reportes en desarrollo")

def main():
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()
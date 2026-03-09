import customtkinter as ctk
import time
import threading
from tkinter import messagebox
import basededatos as db

class UILogin:
    def __init__(self, app):
        self.app = app # Ventana principal

    def mostrar_pantalla_carga(self):
        self.app.limpiar_ventana()
        self.app.set_background("fondo_carga.jpg")
        frame_carga = ctk.CTkFrame(self.app, fg_color="#ffffff", corner_radius=20)
        frame_carga.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(frame_carga, text="Cargando Módulos...", font=("Segoe UI", 24, "bold")).pack(pady=20, padx=40)
        self.progress = ctk.CTkProgressBar(frame_carga, width=400)
        self.progress.pack(pady=10, padx=20)
        self.progress.set(0)
        threading.Thread(target=self.simular_carga).start()

    def simular_carga(self):
        for i in range(101):
            time.sleep(0.01) 
            self.progress.set(i / 100)
            self.app.update_idletasks()
        self.app.after(500, self.mostrar_login)

    def mostrar_login(self):
        self.app.limpiar_ventana()
        self.app.set_background("fondo_login.jpg")
        frame_login = ctk.CTkFrame(self.app, corner_radius=20, width=400, height=450, fg_color="white")
        frame_login.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(frame_login, text="Acceso al Sistema", font=("Segoe UI", 26, "bold"), text_color="#3b8ed0").pack(pady=(40, 10))
        self.entry_user = ctk.CTkEntry(frame_login, placeholder_text="Usuario", width=250, height=40)
        self.entry_user.pack(pady=15)
        self.entry_pass = ctk.CTkEntry(frame_login, placeholder_text="Contraseña", show="*", width=250, height=40)
        self.entry_pass.pack(pady=15)
        
        self.entry_user.bind("<Return>", self.validar_login_ui)
        self.entry_pass.bind("<Return>", self.validar_login_ui)
        
        # La validación ocurrirá directamente en principal pero aquí pasamos la ref
        ctk.CTkButton(frame_login, text="INGRESAR", width=250, height=45, command=self.validar_login_ui).pack(pady=30)

    def validar_login_ui(self, event=None):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        resultado = db.validar_login(user, pwd)
        
        if resultado:
            self.app.usuario_actual = user
            self.app.rol_actual = resultado[0]
            self.app.mostrar_menu_bienvenida()
        else:
            messagebox.showerror("Error", "Usuario o Contraseña incorrectos")

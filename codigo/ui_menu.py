import customtkinter as ctk

class UIMenuPrincipal:
    def __init__(self, app):
        self.app = app

    def mostrar_menu_bienvenida(self):
        self.app.limpiar_ventana()
        self.app.set_background("fondo_app.jpg")
        f_head = ctk.CTkFrame(self.app, height=50, corner_radius=0)
        f_head.pack(fill="x")
        ctk.CTkLabel(f_head, text=f"👤 {self.app.usuario_actual} | {self.app.rol_actual}", padx=20).pack(side="left")
        ctk.CTkButton(f_head, text="Cerrar Sesión", fg_color="#c0392b", width=100, command=self.app.mostrar_login).pack(side="right", padx=10, pady=5)
        
        frame_menu = ctk.CTkFrame(self.app, fg_color=("white", "gray20"), corner_radius=15)
        frame_menu.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(frame_menu, text="MENU PRINCIPAL", font=("Segoe UI", 22, "bold")).pack(pady=30, padx=50)
        
        ctk.CTkButton(frame_menu, text="📝 Nuevo Registro", width=300, height=45, command=lambda: self.app.cargar_interfaz_principal(modo="nuevo")).pack(pady=10)
        ctk.CTkButton(frame_menu, text="🔍 Buscar y Gestionar", width=300, height=45, command=lambda: self.app.cargar_interfaz_principal(modo="buscar")).pack(pady=10)
        ctk.CTkButton(frame_menu, text="📂 Exportar a Excel", width=300, height=45, fg_color="#27ae60", command=self.app.exportar_excel_ui).pack(pady=10)
        
        if self.app.rol_actual == "Administrador":
            ctk.CTkButton(frame_menu, text="💾 Crear Respaldo (Backup)", width=300, height=45, fg_color="#8e44ad", command=self.app.respaldar_bd_ui).pack(pady=10)

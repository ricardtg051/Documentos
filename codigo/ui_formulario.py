import customtkinter as ctk

class UIFormularioPrincipal:
    def __init__(self, app):
        self.app = app

    def cargar_interfaz_principal(self, modo="nuevo"):
        self.app.modo_actual = modo 
        self.app.limpiar_ventana()
        self.app.set_background("fondo_win.jpg")
        
        f_header = ctk.CTkFrame(self.app, fg_color="transparent")
        f_header.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(f_header, text="⬅ Volver", fg_color="#7f8c8d", width=80, command=self.app.mostrar_menu_bienvenida).pack(side="left")
        
        texto_modo = "📝 MODO: NUEVO REGISTRO" if modo == "nuevo" else "🔍 MODO: EDICIÓN Y GESTIÓN"
        color_modo = "#27ae60" if modo == "nuevo" else "#2980b9"
        
        self.app.lbl_modo = ctk.CTkLabel(f_header, text=texto_modo, font=("Segoe UI", 16, "bold"), text_color=color_modo)
        self.app.lbl_modo.pack(side="left", padx=20)
        ctk.CTkButton(f_header, text="❓ AYUDA", fg_color="#f39c12", text_color="white", width=100, font=("bold", 12), command=self.app.mostrar_ayuda).pack(side="right", padx=10)
        
        if modo == "buscar":
            f_busq = ctk.CTkFrame(self.app, fg_color="white", corner_radius=10)
            f_busq.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(f_busq, text="Búsqueda:", font=("bold", 12)).pack(side="left", padx=(15, 5))
            self.app.entry_buscar = ctk.CTkEntry(f_busq, placeholder_text="Escriba nombre o cédula...", height=35)
            self.app.entry_buscar.pack(side="left", padx=5, pady=10, expand=True, fill="x")
            self.app.entry_buscar.bind("<KeyRelease>", self.app.actualizar_busqueda_dinamica)
            
            ctk.CTkButton(f_busq, text="🔍 BUSCAR", width=100, height=35, command=lambda: self.app.cargar_usuario_desde_busqueda(self.app.entry_buscar.get())).pack(side="left", padx=10)
            
            if self.app.rol_actual == "Administrador":
                ctk.CTkButton(f_busq, text="ELIMINAR", width=100, height=35, fg_color="#e74c3c", command=self.app.eliminar_registro_ui).pack(side="right", padx=15)
        else:
            self.app.entry_buscar = None

        self.app.lista_resultados = ctk.CTkScrollableFrame(self.app, height=150, width=500, fg_color="#f8f9f9", corner_radius=5, border_width=1)
        self.app.scroll = ctk.CTkScrollableFrame(self.app, fg_color="transparent")
        self.app.scroll.pack(expand=True, fill="both", padx=10, pady=5)
        self.app.inputs, self.app.combos = {}, {}
        
        f_cols = ctk.CTkFrame(self.app.scroll, fg_color="transparent")
        f_cols.pack(fill="x", expand=True)

        # SECCIÓN IZQUIERDA
        f_izq = ctk.CTkFrame(f_cols, corner_radius=15, fg_color="white")
        f_izq.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        ctk.CTkLabel(f_izq, text="DATOS PERSONALES", font=("bold", 14), text_color="#2980b9").pack(pady=10)
        self.app.crear_input(f_izq, "Nombre Completo", "nombre", placeholder="Ej: Leonardo David Moreno Bruce", val_type="letras")
        row1 = ctk.CTkFrame(f_izq, fg_color="transparent")
        row1.pack(fill="x", padx=15)
        self.app.crear_input(row1, "Cédula", "cedula", pack_side="left", placeholder="Solo números", val_type="numeros")
        self.app.crear_input(row1, "Fecha Nacimiento", "fnac", pack_side="right", placeholder="DD/MM/AAAA", val_type="fecha")
        self.app.crear_input(f_izq, "Correo Electrónico", "correo", placeholder="correo@ejemplo.com")
        self.app.crear_input(f_izq, "Teléfono", "telf", placeholder="04120000000", val_type="numeros")
        self.app.crear_input(f_izq, "Dirección", "dir", placeholder="Calle, Sector, Ciudad")
        ctk.CTkLabel(f_izq, text="Observaciones", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(5,0))
        self.app.txt_obs = ctk.CTkTextbox(f_izq, height=100, border_width=1, border_color="#abb2b9")
        self.app.txt_obs.pack(fill="x", padx=20, pady=(0, 20))

        # SECCIÓN DERECHA
        f_der = ctk.CTkFrame(f_cols, corner_radius=15, fg_color="white")
        f_der.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.crear_seccion_institucional(f_der)

        self.app.cargar_datos_combos_inicial()

        f_btns = ctk.CTkFrame(self.app, fg_color="transparent")
        f_btns.pack(fill="x", padx=20, pady=10)
        
        color_boton = "#27ae60" if self.app.modo_actual == "nuevo" else "#2980b9"
        texto_boton = "💾 GUARDAR" if self.app.modo_actual == "nuevo" else "💾 ACTUALIZAR CAMBIOS"

        self.btn_guardar = ctk.CTkButton(f_btns, text=texto_boton, fg_color=color_boton, 
                                         hover_color="#1e8449" if self.app.modo_actual == "nuevo" else "#1a5276",
                                         height=45, command=self.app.guardar_ui)
        self.btn_guardar.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(f_btns, text="📄 WORD", fg_color="#e67e22", height=45, command=self.app.generar_word_ui).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(f_btns, text="🧹 LIMPIAR TODO", fg_color="#95a5a6", height=45, command=self.app.limpiar_formulario).pack(side="left", expand=True, fill="x", padx=5)

    def crear_seccion_institucional(self, f_der):
        ctk.CTkLabel(f_der, text="DATOS INSTITUCIONALES", font=("bold", 14), text_color="#2980b9").pack(pady=10)
        self.app.crear_combo(f_der, "Universidad", "uni", command=self.app.cargar_especialidades_por_uni)
        self.app.crear_combo(f_der, "Especialidad", "esp")
        self.app.crear_combo(f_der, "Centro de Salud", "cen", command=self.app.actualizar_responsable_en_pantalla)
        
        self.app.lbl_responsable = ctk.CTkLabel(f_der, text="Responsable: (Seleccione un centro)", font=("Segoe UI", 10, "italic"), text_color="#3498db")
        self.app.lbl_responsable.pack(anchor="w", padx=25, pady=(0, 10))

        self.app.crear_combo(f_der, "Guardias Asignadas", "guardias")
        self.app.crear_combo(f_der, "Cargo", "car")
        self.app.crear_combo(f_der, "Modalidad", "mod")
        
        row2 = ctk.CTkFrame(f_der, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=5)
        self.app.crear_input(row2, "Fecha Inicio", "ini", pack_side="left", placeholder="DD/MM/AAAA", val_type="fecha")
        self.app.crear_input(row2, "Fecha Fin", "fin", pack_side="right", placeholder="DD/MM/AAAA", val_type="fecha")

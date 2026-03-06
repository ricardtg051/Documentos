import os
import time
import threading
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

# Importaciones de nuestros nuevos módulos
import database as db
import documentos as docs

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AppFinalPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Registro Médico")
        try:
            self.state("fullscreen") 
        except:
            self.geometry("1200x800") 

        self.usuario_actual = ""
        self.rol_actual = ""
        self.imagenes = {}
        self.modo_actual = "nuevo"
        
        self.vcmd_letra = (self.register(self.validar_letras), '%P')
        self.vcmd_num = (self.register(self.validar_numeros), '%P')
        self.vcmd_fecha = (self.register(self.validar_fecha), '%P')
        
        self.protocol("WM_DELETE_WINDOW", self.confirmar_salida)
        
        # Inicialización de Base de Datos a través del módulo
        db.crear_db()
        db.inicializar_datos_semilla() 
        self.mostrar_pantalla_carga()

    # --- Validaciones y UI General ---
    def validar_letras(self, texto_nuevo):
        if texto_nuevo == "": return True
        return all(char.isalpha() or char.isspace() for char in texto_nuevo)

    def validar_numeros(self, texto_nuevo):
        if texto_nuevo == "": return True
        return texto_nuevo.isdigit()

    def validar_fecha(self, texto_nuevo):
        if texto_nuevo == "": return True
        return all(char.isdigit() or char in "/-" for char in texto_nuevo)

    def set_background(self, nombre_imagen):
        try:
            if nombre_imagen not in self.imagenes:
                img_pil = Image.open(nombre_imagen)
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(w, h))
                self.imagenes[nombre_imagen] = img_ctk
            
            bg_label = ctk.CTkLabel(self, text="", image=self.imagenes[nombre_imagen])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception:
            self.configure(fg_color="#f0f0f0")

    def limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- Pantallas ---
    def mostrar_pantalla_carga(self):
        self.limpiar_ventana()
        self.set_background("fondo_carga.jpg")
        frame_carga = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=20)
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
            self.update_idletasks()
        self.after(500, self.mostrar_login)

    def mostrar_login(self):
        self.limpiar_ventana()
        self.set_background("fondo_login.jpg")
        frame_login = ctk.CTkFrame(self, corner_radius=20, width=400, height=450, fg_color="white")
        frame_login.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(frame_login, text="Acceso al Sistema", font=("Segoe UI", 26, "bold"), text_color="#3b8ed0").pack(pady=(40, 10))
        self.entry_user = ctk.CTkEntry(frame_login, placeholder_text="Usuario", width=250, height=40)
        self.entry_user.pack(pady=15)
        self.entry_pass = ctk.CTkEntry(frame_login, placeholder_text="Contraseña", show="*", width=250, height=40)
        self.entry_pass.pack(pady=15)
        ctk.CTkButton(frame_login, text="INGRESAR", width=250, height=45, command=self.validar_login_ui).pack(pady=30)

    def validar_login_ui(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        
        resultado = db.validar_login(user, pwd)
        
        if resultado:
            self.usuario_actual = user
            self.rol_actual = resultado[0]
            self.mostrar_menu_bienvenida()
        else:
            messagebox.showerror("Error", "Usuario o Contraseña incorrectos")

    def mostrar_menu_bienvenida(self):
        self.limpiar_ventana()
        self.set_background("fondo_app.jpg")
        f_head = ctk.CTkFrame(self, height=50, corner_radius=0)
        f_head.pack(fill="x")
        ctk.CTkLabel(f_head, text=f"👤 {self.usuario_actual} | {self.rol_actual}", padx=20).pack(side="left")
        ctk.CTkButton(f_head, text="Cerrar Sesión", fg_color="#c0392b", width=100, command=self.mostrar_login).pack(side="right", padx=10, pady=5)
        
        frame_menu = ctk.CTkFrame(self, fg_color=("white", "gray20"), corner_radius=15)
        frame_menu.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(frame_menu, text="MENU PRINCIPAL", font=("Segoe UI", 22, "bold")).pack(pady=30, padx=50)
        ctk.CTkButton(frame_menu, text="📝 Nuevo Registro", width=300, height=55, command=lambda: self.cargar_interfaz_principal(modo="nuevo")).pack(pady=10)
        ctk.CTkButton(frame_menu, text="🔍 Buscar y Gestionar", width=300, height=55, command=lambda: self.cargar_interfaz_principal(modo="buscar")).pack(pady=10)
        ctk.CTkButton(frame_menu, text="📂 Exportar a Excel", width=300, height=55, fg_color="#27ae60", command=self.exportar_excel_ui).pack(pady=10)

    def cargar_interfaz_principal(self, modo="nuevo"):
        self.modo_actual = modo 
        self.limpiar_ventana()
        self.set_background("fondo_win.jpg")
        
        f_header = ctk.CTkFrame(self, fg_color="transparent")
        f_header.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(f_header, text="⬅ Volver", fg_color="#7f8c8d", width=80, command=self.mostrar_menu_bienvenida).pack(side="left")
        
        texto_modo = "📝 MODO: NUEVO REGISTRO" if modo == "nuevo" else "🔍 MODO: EDICIÓN Y GESTIÓN"
        color_modo = "#27ae60" if modo == "nuevo" else "#2980b9"
        
        self.lbl_modo = ctk.CTkLabel(f_header, text=texto_modo, font=("Segoe UI", 16, "bold"), text_color=color_modo)
        self.lbl_modo.pack(side="left", padx=20)
        ctk.CTkButton(f_header, text="❓ AYUDA", fg_color="#f39c12", text_color="white", width=100, font=("bold", 12), command=self.mostrar_ayuda).pack(side="right", padx=10)
        
        if modo == "buscar":
            f_busq = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
            f_busq.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(f_busq, text="Búsqueda:", font=("bold", 12)).pack(side="left", padx=(15, 5))
            self.entry_buscar = ctk.CTkEntry(f_busq, placeholder_text="Escriba nombre o cédula...", height=35)
            self.entry_buscar.pack(side="left", padx=5, pady=10, expand=True, fill="x")
            self.entry_buscar.bind("<KeyRelease>", self.actualizar_busqueda_dinamica)
            
            ctk.CTkButton(f_busq, text="🔍 BUSCAR", width=100, height=35, command=lambda: self.cargar_usuario_desde_busqueda(self.entry_buscar.get())).pack(side="left", padx=10)
            
            if self.rol_actual == "Administrador":
                ctk.CTkButton(f_busq, text="ELIMINAR", width=100, height=35, fg_color="#e74c3c", command=self.eliminar_registro_ui).pack(side="right", padx=15)
        else:
            self.entry_buscar = None

        self.lista_resultados = ctk.CTkScrollableFrame(self, height=150, width=500, fg_color="#f8f9f9", corner_radius=5, border_width=1)
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(expand=True, fill="both", padx=10, pady=5)
        self.inputs, self.combos = {}, {}
        
        f_cols = ctk.CTkFrame(self.scroll, fg_color="transparent")
        f_cols.pack(fill="x", expand=True)

        # SECCIÓN IZQUIERDA
        f_izq = ctk.CTkFrame(f_cols, corner_radius=15, fg_color="white")
        f_izq.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        ctk.CTkLabel(f_izq, text="DATOS PERSONALES", font=("bold", 14), text_color="#2980b9").pack(pady=10)
        self.crear_input(f_izq, "Nombre Completo", "nombre", placeholder="Ej: Leonardo David Moreno Bruce", val_type="letras")
        row1 = ctk.CTkFrame(f_izq, fg_color="transparent")
        row1.pack(fill="x", padx=15)
        self.crear_input(row1, "Cédula", "cedula", pack_side="left", placeholder="Solo números", val_type="numeros")
        self.crear_input(row1, "Fecha Nacimiento", "fnac", pack_side="right", placeholder="DD/MM/AAAA", val_type="fecha")
        self.crear_input(f_izq, "Correo Electrónico", "correo", placeholder="correo@ejemplo.com")
        self.crear_input(f_izq, "Teléfono", "telf", placeholder="04120000000", val_type="numeros")
        self.crear_input(f_izq, "Dirección", "dir", placeholder="Calle, Sector, Ciudad")
        ctk.CTkLabel(f_izq, text="Observaciones", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20, pady=(5,0))
        self.txt_obs = ctk.CTkTextbox(f_izq, height=100, border_width=1, border_color="#abb2b9")
        self.txt_obs.pack(fill="x", padx=20, pady=(0, 20))

        # SECCIÓN DERECHA
        f_der = ctk.CTkFrame(f_cols, corner_radius=15, fg_color="white")
        f_der.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.crear_seccion_institucional(f_der)

        self.cargar_datos_combos_inicial()

        f_btns = ctk.CTkFrame(self, fg_color="transparent")
        f_btns.pack(fill="x", padx=20, pady=10)
        
        color_boton = "#27ae60" if self.modo_actual == "nuevo" else "#2980b9"
        texto_boton = "💾 GUARDAR" if self.modo_actual == "nuevo" else "💾 ACTUALIZAR CAMBIOS"

        self.btn_guardar = ctk.CTkButton(f_btns, text=texto_boton, fg_color=color_boton, 
                                         hover_color="#1e8449" if self.modo_actual == "nuevo" else "#1a5276",
                                         height=45, command=self.guardar_ui)
        self.btn_guardar.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkButton(f_btns, text="📄 WORD", fg_color="#e67e22", height=45, command=self.generar_word_ui).pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(f_btns, text="🧹 LIMPIAR TODO", fg_color="#95a5a6", height=45, command=self.limpiar_formulario).pack(side="left", expand=True, fill="x", padx=5)

    def crear_seccion_institucional(self, f_der):
        ctk.CTkLabel(f_der, text="DATOS INSTITUCIONALES", font=("bold", 14), text_color="#2980b9").pack(pady=10)
        self.crear_combo(f_der, "Universidad", "uni", command=self.cargar_especialidades_por_uni)
        self.crear_combo(f_der, "Especialidad", "esp")
        self.crear_combo(f_der, "Centro de Salud", "cen", command=self.actualizar_responsable_en_pantalla)
        
        self.lbl_responsable = ctk.CTkLabel(f_der, text="Responsable: (Seleccione un centro)", font=("Segoe UI", 10, "italic"), text_color="#3498db")
        self.lbl_responsable.pack(anchor="w", padx=25, pady=(0, 10))

        self.crear_combo(f_der, "Guardias Asignadas", "guardias")
        self.crear_combo(f_der, "Cargo", "car")
        self.crear_combo(f_der, "Modalidad", "mod")
        
        row2 = ctk.CTkFrame(f_der, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=5)
        self.crear_input(row2, "Fecha Inicio", "ini", pack_side="left", placeholder="DD/MM/AAAA", val_type="fecha")
        self.crear_input(row2, "Fecha Fin", "fin", pack_side="right", placeholder="DD/MM/AAAA", val_type="fecha")

    # --- Lógica de Interacción ---
    def crear_input(self, master, label, key, pack_side=None, placeholder="", val_type=None):
        if pack_side:
            f = ctk.CTkFrame(master, fg_color="transparent"); f.pack(side=pack_side, expand=True, fill="x", padx=2)
            master = f
        ctk.CTkLabel(master, text=label, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20)
        entry = ctk.CTkEntry(master, height=30, placeholder_text=placeholder)
        if val_type == "letras": entry.configure(validate="key", validatecommand=self.vcmd_letra)
        elif val_type == "numeros": entry.configure(validate="key", validatecommand=self.vcmd_num)
        elif val_type == "fecha": entry.configure(validate="key", validatecommand=self.vcmd_fecha)
        self.inputs[key] = entry
        entry.pack(fill="x", padx=20, pady=(0, 10))

        if key == "cedula":
            entry.bind("<FocusOut>", self.verificar_cedula_existente)

    def crear_combo(self, master, label, key, command=None):
        ctk.CTkLabel(master, text=label, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20)
        self.combos[key] = ctk.CTkComboBox(master, height=30, state="readonly", command=command)
        self.combos[key].pack(fill="x", padx=20, pady=(0, 10))

    def cargar_datos_combos_inicial(self):
        self.combos["uni"].configure(values=db.obtener_opciones("universidades"))
        self.combos["cen"].configure(values=db.obtener_opciones("centros"))
        self.combos["car"].configure(values=db.obtener_opciones("cargos"))
        self.combos["mod"].configure(values=db.obtener_opciones("modalidades"))

    def cargar_especialidades_por_uni(self, uni):
        res = db.obtener_opciones("oferta_academica", "especialidad", "universidad", uni)
        self.combos["esp"].configure(values=res)
        if res: self.combos["esp"].set(res[0])

    def cargar_guardias_por_centro(self, centro):
        res = db.obtener_opciones("guardias_centro", "guardia", "centro", centro)
        self.combos["guardias"].configure(values=res)
        if res: self.combos["guardias"].set(res[0])

    def actualizar_responsable_en_pantalla(self, centro_seleccionado):
        self.cargar_guardias_por_centro(centro_seleccionado)
        nombre = db.obtener_responsable_centro(centro_seleccionado)
        
        if nombre:
            self.lbl_responsable.configure(text=f"✅ Responsable: {nombre}", text_color="#27ae60")
        else:
            self.lbl_responsable.configure(text="⚠️ Centro sin responsable asignado", text_color="#e74c3c")

    def actualizar_busqueda_dinamica(self, event=None):
        if not hasattr(self, 'entry_buscar') or self.entry_buscar is None: return
        texto = self.entry_buscar.get().strip()
        for widget in self.lista_resultados.winfo_children(): widget.destroy()
        if texto == "":
            self.lista_resultados.place_forget()
            return
            
        res = db.buscar_usuarios_dinamico(texto)
        
        if res:
            self.lista_resultados.place(x=self.entry_buscar.winfo_rootx() - self.winfo_rootx(), 
                                        y=(self.entry_buscar.winfo_rooty() - self.winfo_rooty()) + 40)
            self.lista_resultados.lift()
            for ced, nom in res:
                btn = ctk.CTkButton(self.lista_resultados, text=f"{ced} - {nom}", fg_color="transparent", 
                                    text_color="black", anchor="w", hover_color="#d5dbdb", 
                                    command=lambda c=ced: self.cargar_usuario_desde_busqueda(c))
                btn.pack(fill="x", pady=1)
        else:
            self.lista_resultados.place_forget()

    def cargar_usuario_desde_busqueda(self, parametro):
        self.lista_resultados.place_forget()
        if not parametro: return
        
        u = db.obtener_usuario(parametro)
        if u:
            self.limpiar_formulario()
            self.entry_buscar.delete(0, 'end'); self.entry_buscar.insert(0, u[0])
            campos = ["cedula","nombre","telf","correo","fnac","dir"]
            for i, k in enumerate(campos): self.inputs[k].insert(0, u[i])
            self.inputs["ini"].insert(0, u[12]); self.inputs["fin"].insert(0, u[13])
            if len(u) > 14 and u[14]: self.txt_obs.insert("1.0", u[14])
            
            self.combos["uni"].set(u[7]); self.cargar_especialidades_por_uni(u[7])
            self.combos["esp"].set(u[8]); self.combos["cen"].set(u[11])
            self.cargar_guardias_por_centro(u[11]); self.combos["guardias"].set(u[6])
            self.combos["car"].set(u[9]); self.combos["mod"].set(u[10])
        else:
            messagebox.showinfo("Búsqueda", "No se encontraron resultados.")
    
    def verificar_cedula_existente(self, event=None):
        cedula = self.inputs["cedula"].get().strip()
        if not cedula: return
        
        nombre_existente = db.verificar_cedula(cedula)
        if nombre_existente:
            self.after(100, lambda: messagebox.showwarning(
                "Cédula Duplicada", f"La cédula {cedula} ya está registrada a nombre de {nombre_existente}."
            ))

    def guardar_ui(self):
        d = {k: v.get().strip() for k, v in self.inputs.items()}
        c = {k: v.get() for k, v in self.combos.items()}
        obs = self.txt_obs.get("1.0", "end-1c").strip()
        
        if not d["cedula"] or not d["nombre"]:
            messagebox.showwarning("Atención", "Nombre y Cédula son obligatorios.")
            return

        if "@" not in d["correo"] or "." not in d["correo"]:
            self.inputs["correo"].configure(border_color="#e74c3c", border_width=2)
            messagebox.showerror("Correo Inválido", "El formato del correo es incorrecto.")
            return
        else:
            self.inputs["correo"].configure(border_color="#abb2b9", border_width=1)
            
        if len(d["telf"]) < 10:
            messagebox.showerror("Teléfono Inválido", "El número de teléfono parece estar incompleto.")
            return
            
        try:
            nombre_existente = db.verificar_cedula(d["cedula"])
            
            if self.modo_actual == "nuevo":
                if nombre_existente:
                    messagebox.showerror("Error", f"La cédula {d['cedula']} ya está registrada.\nPara editarlo, use Búsqueda.")
                    return
                db.guardar_nuevo_usuario(d, c, obs)
                messagebox.showinfo("Éxito", "¡Registro creado exitosamente!")

            else:
                if nombre_existente:
                    db.actualizar_usuario(d, c, obs)
                    messagebox.showinfo("Actualizado", "Los cambios han sido guardados correctamente.")
                else:
                    if messagebox.askyesno("Nuevo Registro", "Esta cédula no existe. ¿Desea crear un nuevo registro?"):
                        db.guardar_nuevo_usuario(d, c, obs)
                        messagebox.showinfo("Éxito", "¡Registro creado exitosamente!")

        except Exception as e: 
            messagebox.showerror("Error de BD", f"Error: {str(e)}")

    def generar_word_ui(self):
        try:
            ced = self.inputs["cedula"].get().strip()
            centro_actual = self.combos["cen"].get()
            
            if not ced: 
                messagebox.showwarning("Atención", "Debe ingresar una cédula para generar el documento.")
                return

            datos_pantalla = {k: v.get().strip() for k, v in self.inputs.items()}
            combos_pantalla = {k: v.get() for k, v in self.combos.items()}
            obs_pantalla = self.txt_obs.get("1.0", "end-1c").strip()

            u = db.obtener_usuario(ced)
            datos_guardados = False
            if u:
                match = (str(u[0]) == datos_pantalla["cedula"] and str(u[1]) == datos_pantalla["nombre"] and
                         str(u[11]) == combos_pantalla["cen"] and str(u[14] if u[14] else "") == obs_pantalla)
                if match: datos_guardados = True

            if not datos_guardados:
                if not messagebox.askyesno("Datos no Guardados", "¿Desea generar el Word con los datos de la pantalla de todos modos?"):
                    return

            responsable = db.obtener_responsable_centro(centro_actual)
            docs.generar_documento_word(datos_pantalla, combos_pantalla, obs_pantalla, responsable)
            
        except Exception as e: 
            messagebox.showerror("Error", f"No se pudo generar el Word: {e}")

    def limpiar_formulario(self):
        for e in self.inputs.values(): e.delete(0, 'end')
        for c in self.combos.values(): c.set("")
        self.txt_obs.delete("1.0", "end")
        self.lista_resultados.place_forget()

    def mostrar_ayuda(self):
        msj_actual = db.obtener_mensaje_ayuda()
        ventana_ayuda = ctk.CTkToplevel(self)
        ventana_ayuda.title("Centro de Ayuda")
        ventana_ayuda.geometry("550x400")
        ventana_ayuda.transient(self)
        ventana_ayuda.grab_set()
        ctk.CTkLabel(ventana_ayuda, text="Centro de ayuda:", font=("Segoe UI", 14, "bold")).pack(pady=(20, 10))
        caja_texto = ctk.CTkTextbox(ventana_ayuda, width=500, height=250, border_width=1, border_color="#abb2b9")
        caja_texto.pack(pady=10, padx=20)
        caja_texto.insert("1.0", msj_actual)

    def eliminar_registro_ui(self):
        ced = self.inputs["cedula"].get()
        if ced and messagebox.askyesno("Confirmar", "¿Eliminar registro?"):
            db.eliminar_usuario(ced)
            self.limpiar_formulario()

    def exportar_excel_ui(self):
        try:
            docs.exportar_excel_db()
        except Exception as e: 
            messagebox.showerror("Excel Error", str(e))

    def confirmar_salida(self): self.destroy()

if __name__ == "__main__":
    app = AppFinalPro()
    app.mainloop()

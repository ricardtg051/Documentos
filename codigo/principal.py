import os
import time
import threading
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

# Importaciones de nuestros nuevos módulos
import basededatos as db
import documentos as docs

from ui_login import UILogin
from ui_menu import UIMenuPrincipal
from ui_formulario import UIFormularioPrincipal

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
        
        self.login_ui = UILogin(self)
        self.menu_ui = UIMenuPrincipal(self)
        self.form_ui = UIFormularioPrincipal(self)
        
        # Inicialización de Base de Datos a través del módulo
        db.crear_db()
        db.inicializar_datos_semilla() 
        self.mostrar_pantalla_carga()

    # --- Validaciones y UI General ---
    def validar_letras(self, texto_nuevo):
        # Ayudamos al sistema a no bloquear las propias instrucciones grises
        if texto_nuevo == "" or texto_nuevo == "Ej: Leonardo David Moreno Bruce": return True
        return all(char.isalpha() or char.isspace() for char in texto_nuevo)

    def validar_numeros(self, texto_nuevo):
        if texto_nuevo == "" or texto_nuevo == "Solo números" or texto_nuevo == "04120000000": return True
        return texto_nuevo.isdigit()

    def validar_fecha(self, texto_nuevo):
        if texto_nuevo == "" or texto_nuevo == "DD/MM/AAAA": return True
        return all(char.isdigit() or char in "/-" for char in texto_nuevo)

    def auto_formatear_fecha(self, event, widget_entry):
        if event.keysym in ("BackSpace", "Delete", "Left", "Right"): return
        texto = widget_entry.get()
        numeros = "".join(filter(str.isdigit, texto))
        if len(numeros) > 8: numeros = numeros[:8]
        res = ""
        for i, n in enumerate(numeros):
            if i in (2, 4): res += "/"
            res += n
        if widget_entry.get() != res:
            widget_entry.delete(0, 'end')
            widget_entry.insert(0, res)

    def set_background(self, nombre_imagen):
        import os
        ruta_imagen = os.path.join("imagenes", nombre_imagen)
        try:
            if nombre_imagen not in self.imagenes:
                img_pil = Image.open(ruta_imagen)
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

    def mostrar_pantalla_carga(self):
        self.login_ui.mostrar_pantalla_carga()

    def mostrar_login(self):
        self.login_ui.mostrar_login()

    def mostrar_menu_bienvenida(self):
        self.menu_ui.mostrar_menu_bienvenida()

    def cargar_interfaz_principal(self, modo="nuevo"):
        self.form_ui.cargar_interfaz_principal(modo)

    # --- Lógica de Interacción ---
    def crear_input(self, master, label, key, pack_side=None, placeholder="", val_type=None):
        if pack_side:
            f = ctk.CTkFrame(master, fg_color="transparent"); f.pack(side=pack_side, expand=True, fill="x", padx=2)
            master = f
        ctk.CTkLabel(master, text=label, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=20)
        
        entry = ctk.CTkEntry(master, height=30, placeholder_text=placeholder)
        
        if val_type == "letras": entry.configure(validate="key", validatecommand=self.vcmd_letra)
        elif val_type == "numeros": entry.configure(validate="key", validatecommand=self.vcmd_num)
        elif val_type == "fecha": 
            entry.configure(validate="key", validatecommand=self.vcmd_fecha)
            entry.bind("<KeyRelease>", lambda e, w=entry: self.auto_formatear_fecha(e, w))
            
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
        
        # --- VALIDACIONES NUEVAS (No dejar vacio ni fechas malas) ---
        # Validar que no existan campos de texto vacios
        for clave, valor in d.items():
            if valor == "":
                messagebox.showwarning("Atención", "No puede dejar ningún campo en blanco. Llénelos todos por favor.")
                return
                
        # Validar los campos de seleccion (combos)
        for clave, valor in c.items():
            if valor == "":
                messagebox.showwarning("Atención", "Debe seleccionar una opción en todas las listas.")
                return

        # Validar que las fechas no den fallas usando time
        fechas = [d["fnac"], d["ini"], d["fin"]]
        for f in fechas:
            try:
                # Comprobamos que tenga el formato de fecha exacto
                time.strptime(f, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Fecha incorrecta", "La fecha ingresada tiene fallas. Por favor corríjala usando el formato: DD/MM/AAAA (Ejemplo: 25/08/2020)")
                return

        # --- Fin de validaciones nuevas ---

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
        for e in self.inputs.values(): 
            e.delete(0, 'end')
        for c in self.combos.values(): c.set("")
        self.txt_obs.delete("1.0", "end")
        self.lista_resultados.place_forget()
        self.focus() # Quitamos el foco seleccionando la ventana principal

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

    def respaldar_bd_ui(self):
        import time
        from tkinter import filedialog
        
        # Generar nombre por defecto con fecha
        fecha_str = time.strftime("%d_%m_%Y_%H%M")
        nombre_default = f"Respaldo_BD_{fecha_str}.db"
        
        # Abrir ventana para que el usuario escoja donde guardar
        ruta = filedialog.asksaveasfilename(
            defaultextension=".db",
            initialfile=nombre_default,
            title="Guardar Respaldo de Base de Datos",
            filetypes=[("Archivos de Base de Datos", "*.db"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            exito = db.hacer_respaldo_bd(ruta)
            if exito:
                messagebox.showinfo("Respaldo Exitoso", f"La base de datos completa se ha guardado correctamente como una copia de seguridad en:\n{ruta}")
            else:
                messagebox.showerror("Error", "No se encontró el archivo original de la base de datos para copiar.")

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

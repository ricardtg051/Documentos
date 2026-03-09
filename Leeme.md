# Sistema de Registro Médico ("AppFinalPro")

Este es el repositorio del Sistema de Registro Médico, una herramienta sencilla que hice en Python para registrar, buscar y exportar datos del personal de salud. Usa `customtkinter` para la interfaz gráfica y SQLite para guardar la información.

## ⚙️ ¿Qué necesitas para correrlo?

Asegúrate de tener Python 3 instalado. Luego, instala las librerías que usé en el proyecto ejecutando esto en tu terminal:

```bash
pip install customtkinter pandas docxtpl openpyxl Pillow
```

## 🚀 ¿Cómo se usa?

1. Fíjate que en la misma carpeta del proyecto tengas todos los archivos juntos:
   - Los scripts `main.py`, `database.py` y `documentos.py`.
   - La base de datos `database_final.db` (¡no la borres o pierdes los datos!).
   - El archivo `plantilla.docx` (se usa para generar los expedientes).
   - Las imágenes de fondo (`fondo_app.jpg`, `fondo_carga.jpg`, `fondo_login.jpg`).
2. Abre tu terminal ahí, y arranca el programa con:
   ```bash
   python main.py
   ```
3. Cuando te pida usuario y contraseña, ingresa con **admin** en ambos (usuario: `admin`, clave: `admin`).

---

## 📖 Manual Rápido (Cómo hacer las cosas básicas)

### 📝 1. Agregar a alguien nuevo
- Entra a **"📝 Nuevo Registro"** en el menú principal.
- Llena los datos que te piden (Cédula, correo, universidad, etc.). Ojo con los correos y las cédulas, el sistema valida que estén bien escritos y que la cédula no se repita.
- Dale al botón verde **"💾 GUARDAR"** abajo y listo.

### 🔍 2. Buscar, Editar (o Eliminar)
- En el menú, elige **"🔍 Buscar y Gestionar"**.
- Arriba hay una barra de búsqueda: pon la cédula o el nombre y te saldrán los resultados dinámicamente. Dale clic al que necesitas.
- Vas a ver que todos sus datos se cargan solitos en el formulario. Cámbiales lo que necesites y dale a **"💾 ACTUALIZAR CAMBIOS"**.
- Si entraste como administrador (con la cuenta `admin`), vas a ver un botón rojo que dice **"ELIMINAR"** por si te equivocaste y quieres borrar ese registro.

### 📄 3. Sacar un Reporte en Word
Si necesitas imprimirle el expediente a alguien:
- Búscalo en el sistema para que sus datos aparezcan en pantalla.
- Dale al botón naranja **"📄 WORD"**.
- El sistema automáticamente va a agarrar el archivo `plantilla.docx`, va a rellenar sus datos, te va a crear un archivo nuevo como `Expediente_1234567.docx`, y lo va a abrir.

### 📂 4. Exportar toodos los datos del sistema
Si necesitas pasarle el reporte a logística o algo, ve al menú principal y dale a **"📂 Exportar a Excel"**. Se va a crear un archivo que se llama `Base_Datos.xlsx` con todo lo que hay guardado en la base de datos hasta ese momento.

### 💾 5. Hacer Respaldo (Backup) y Restaurarlo
Si tienes el rol de "Administrador", verás un botón morado que dice **"💾 Crear Respaldo (Backup)"**. Úsalo cada cierto tiempo para guardar una copia exacta y segura de toda la base de datos en tu pendrive o disco duro. Solo dale clic y elige dónde quieres guardarlo.
* **¿Cómo restaurarlo o usarlo en otra PC?** Muy fácil. Tomas el archivo `.db` que acabas de guardar en tu pendrive, lo llevas a la otra computadora, y lo renombras a `database_final.db`. Luego, simplemente reemplazas (pegas y sobrescribes) ese archivo en la misma carpeta donde tienes a `main.py`. Cuando abras el programa de nuevo, ¡listo! ya tendrás ahí todos los datos.

### 💡 Unos atajos extra
- Si estabas viendo los datos de alguien y quieres vaciar la pantalla para agregar a alguien más de cero, dale al botón gris **"🧹 LIMPIAR TODO"**.
- Si se te olvida algo de esto, dentro del formulario hay un botón amarillo de **"❓ AYUDA"**. Dale ahí y te sale un resumen rápido.

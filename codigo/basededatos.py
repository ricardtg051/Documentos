import sqlite3
import os

DB_PATH = os.path.join("bases_de_datos", "database_final.db")

def ejecutar_consulta(query, parametros=(), fetch=False, fetchall=False):
    """Función auxiliar para manejar la conexión a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute(query, parametros)
        if fetch:
            if fetchall:
                resultado = cursor.fetchall()
            else:
                resultado = cursor.fetchone()
            return resultado
        
        conn.commit()
    finally:
        conn.close()

def crear_db():
    queries = [
        "CREATE TABLE IF NOT EXISTS login_users (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT UNIQUE, password TEXT, rol TEXT)",
        """CREATE TABLE IF NOT EXISTS usuarios 
           (id INTEGER PRIMARY KEY AUTOINCREMENT, cedula TEXT UNIQUE, nombre TEXT, telf TEXT, correo TEXT, fnac TEXT, dir TEXT, guardias TEXT,
           uni TEXT, esp TEXT, car TEXT, mod TEXT, cen TEXT, ini TEXT, fin TEXT, observaciones TEXT)""",
        "CREATE TABLE IF NOT EXISTS centros (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE, responsable TEXT)",
        "CREATE TABLE IF NOT EXISTS oferta_academica (id INTEGER PRIMARY KEY AUTOINCREMENT, universidad TEXT, especialidad TEXT, UNIQUE(universidad, especialidad))",
        "CREATE TABLE IF NOT EXISTS guardias_centro (id INTEGER PRIMARY KEY AUTOINCREMENT, centro TEXT, guardia TEXT, UNIQUE(centro, guardia))",
        "CREATE TABLE IF NOT EXISTS universidades (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)",
        "CREATE TABLE IF NOT EXISTS cargos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)",
        "CREATE TABLE IF NOT EXISTS modalidades (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)",
        "CREATE TABLE IF NOT EXISTS configuracion (id INTEGER PRIMARY KEY AUTOINCREMENT, clave TEXT UNIQUE, valor TEXT)"
    ]
    for q in queries:
        ejecutar_consulta(q)
    
    # Manejar actualización de tabla por si no existe la columna
    try:
        ejecutar_consulta("ALTER TABLE usuarios ADD COLUMN observaciones TEXT")
    except sqlite3.OperationalError:
        pass

def inicializar_datos_semilla():
    ejecutar_consulta("INSERT OR IGNORE INTO login_users (usuario, password, rol) VALUES ('admin', 'admin', 'Administrador')")
    msj_defecto = ("🆘 SOPORTE DEL SISTEMA\n\n"
                   "1. BÚSQUEDA: Escriba y use la lista desplegable o el botón 🔍.\n"
                   "2. GUARDAR: Presione el botón verde. Los datos se mantienen para generar el Word.\n"
                   "3. WORD: Requiere el archivo 'plantilla.docx' en la misma carpeta.\n"
                   "4. LIMPIAR: Use el botón gris si desea registrar a otra persona desde cero.")
    ejecutar_consulta("INSERT OR IGNORE INTO configuracion (clave, valor) VALUES ('mensaje_ayuda', ?)", (msj_defecto,))

def validar_login(user, pwd):
    return ejecutar_consulta("SELECT rol FROM login_users WHERE usuario=? AND password=?", (user, pwd), fetch=True)

def obtener_mensaje_ayuda():
    res = ejecutar_consulta("SELECT valor FROM configuracion WHERE clave = 'mensaje_ayuda'", fetch=True)
    if res:
        return res[0]
    else:
        return "Escriba aquí la ayuda..."

def buscar_usuarios_dinamico(texto):
    return ejecutar_consulta("SELECT cedula, nombre FROM usuarios WHERE cedula LIKE ? OR nombre LIKE ? LIMIT 5", 
                             (f'%{texto}%', f'%{texto}%'), fetch=True, fetchall=True)

def obtener_usuario(parametro):
    # Ya que ahora usamos un ID autonumerico para la primary key, traemos todo pero filtramos 
    return ejecutar_consulta("SELECT cedula, nombre, telf, correo, fnac, dir, guardias, uni, esp, car, mod, cen, ini, fin, observaciones FROM usuarios WHERE cedula = ? OR nombre = ?", (parametro, parametro), fetch=True)

def verificar_cedula(cedula):
    res = ejecutar_consulta("SELECT nombre FROM usuarios WHERE cedula = ?", (cedula,), fetch=True)
    if res:
        return res[0]
    else:
        return None

def obtener_responsable_centro(centro):
    res = ejecutar_consulta("SELECT responsable FROM centros WHERE nombre = ?", (centro,), fetch=True)
    if res:
        return res[0]
    else:
        return None

def obtener_opciones(tabla, columna="nombre", filtro_col=None, filtro_val=None):
    if filtro_col and filtro_val:
        query = f"SELECT {columna} FROM {tabla} WHERE {filtro_col} = ?"
        res = ejecutar_consulta(query, (filtro_val,), fetch=True, fetchall=True)
    else:
        query = f"SELECT {columna} FROM {tabla}"
        res = ejecutar_consulta(query, fetch=True, fetchall=True)
        
    if res:
        lista_opciones = []
        for fila in res:
            lista_opciones.append(fila[0])
        return lista_opciones
    else:
        return []

def guardar_nuevo_usuario(d, c, obs):
    ejecutar_consulta("""INSERT INTO usuarios 
        (cedula, nombre, telf, correo, fnac, dir, guardias, uni, esp, car, mod, cen, ini, fin, observaciones) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", 
        (d["cedula"], d["nombre"], d["telf"], d["correo"], d["fnac"], d["dir"], c["guardias"],
         c["uni"], c["esp"], c["car"], c["mod"], c["cen"], d["ini"], d["fin"], obs))

def actualizar_usuario(d, c, obs):
    ejecutar_consulta("""UPDATE usuarios SET 
        nombre=?, telf=?, correo=?, fnac=?, dir=?, guardias=?, uni=?, 
        esp=?, car=?, mod=?, cen=?, ini=?, fin=?, observaciones=? 
        WHERE cedula=?""", 
        (d["nombre"], d["telf"], d["correo"], d["fnac"], d["dir"], c["guardias"],
         c["uni"], c["esp"], c["car"], c["mod"], c["cen"], d["ini"], d["fin"], obs, d["cedula"]))

def eliminar_usuario(cedula):
    ejecutar_consulta("DELETE FROM usuarios WHERE cedula=?", (cedula,))

def hacer_respaldo_bd(ruta_destino):
    import shutil
    import os
    if os.path.exists(DB_PATH):
        # Aqui generamos la copia del archivo exacto de la base de datos
        shutil.copy2(DB_PATH, ruta_destino)
        return True
    return False
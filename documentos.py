import os
import pandas as pd
from docxtpl import DocxTemplate
from datetime import datetime
import sqlite3
from database import DB_PATH

def exportar_excel_db():
    """Conecta a la BD, lee los usuarios y exporta a Excel."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM usuarios", conn)
    conn.close()
    
    nombre_archivo = "Base_Datos.xlsx"
    df.to_excel(nombre_archivo, index=False)
    os.startfile(nombre_archivo)

def generar_documento_word(datos_inputs, datos_combos, observaciones, responsable):
    """Recibe diccionarios con la información de la UI y genera el Word."""
    doc = DocxTemplate("plantilla.docx")
    
    # Combinar los diccionarios para el contexto
    ctx = {**datos_inputs, **datos_combos}
    ctx["observaciones"] = observaciones
    ctx["fecha_actual"] = datetime.now().strftime("%d/%m/%Y")
    ctx["responsable_centro"] = responsable if responsable else "No Asignado"
    
    doc.render(ctx)
    cedula = datos_inputs.get("cedula", "Desconocido")
    nombre_arc = f"Expediente_{cedula}.docx"
    doc.save(nombre_arc)
    os.startfile(nombre_arc)
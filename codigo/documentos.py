import os
import shutil
import pandas as pd
from docxtpl import DocxTemplate
from datetime import datetime # Added this import as it's used later

def exportar_excel_db():
    """Conecta a la BD, lee los usuarios y exporta a Excel."""
    import sqlite3
    import pandas as pd
    import os
    from basededatos import DB_PATH
    
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM usuarios", conn)
    conn.close()
    
    # Nombre y ruta más acertados
    nombre_archivo = os.path.join("bases_de_datos", "Reporte_General_Residentes.xlsx")
    
    # Exportar y abrir
    df.to_excel(nombre_archivo, index=False)
    os.startfile(nombre_archivo)



def generar_documento_word(datos_inputs, datos_combos, observaciones, responsable):
    """Recibe diccionarios con la información de la UI y genera el Word."""
    doc = DocxTemplate("plantilla.docx")
    
    # Combinar los diccionarios para el contexto sin usar metodos avanzados
    ctx = {}
    for clave, valor in datos_inputs.items():
        ctx[clave] = valor
    for clave, valor in datos_combos.items():
        ctx[clave] = valor
        
    ctx["observaciones"] = observaciones
    ctx["fecha_actual"] = datetime.now().strftime("%d/%m/%Y")
    
    if responsable:
        ctx["responsable_centro"] = responsable
    else:
        ctx["responsable_centro"] = "No Asignado"
    
    doc.render(ctx)
    cedula = datos_inputs.get("cedula", "Desconocido")
    nombre_arc = f"Expediente_{cedula}.docx"
    doc.save(nombre_arc)
    os.startfile(nombre_arc)
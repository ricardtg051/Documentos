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

    # The following loop and dictionary creation seems to be preparing data for a document,
    # not directly for an Excel export as the function name suggests.
    # This part of the instruction is applied as given, but it doesn't complete an Excel export.
    for r in listado_resultados:
        dicccionario_datos = {
            "cedula": r[0] if r[0] else "",
            "nombre": r[1] if r[1] else "",
            "telf": r[2] if r[2] else "",
            "correo": r[3] if r[3] else "",
            "fnac": r[4] if r[4] else "",
            "dir": r[5] if r[5] else "",
            "guardias": r[6] if r[6] else "",
            "uni": r[7] if r[7] else "",
            "esp": r[8] if r[8] else "",
            "car": r[9] if r[9] else "",
            "mod": r[10] if r[10] else "",
            "cen": r[11] if r[11] else "",
            "ini": r[12] if r[12] else "",
            "fin": r[13] if r[13] else "",
            "observaciones": r[14] if r[14] else ""
        }
    # Note: dicccionario_datos will only contain the last record's data after this loop.
    # The function as modified by the instruction is incomplete for its stated purpose.


def generar_documento_word(datos_inputs, datos_combos, observaciones, responsable):
    """Recibe diccionarios con la información de la UI y genera el Word."""
    doc = DocxTemplate("plantilla.docx")
    
    # Combinar los diccionarios para el contexto
    ctx = {**datos_inputs, **datos_combos}
    ctx["observaciones"] = observaciones
    # The following lines are from the instruction's code edit,
    # which were placed after the `for r in listado_resultados:` loop.
    # They logically belong here in `generar_documento_word`.
    ctx["fecha_actual"] = datetime.now().strftime("%d/%m/%Y") # This line was already present, but also in the instruction's snippet.
    ctx["responsable_centro"] = responsable if responsable else "No Asignado" # This line was already present, but also in the instruction's snippet.
    
    doc.render(ctx)
    cedula = datos_inputs.get("cedula", "Desconocido")
    nombre_arc = f"Expediente_{cedula}.docx"
    doc.save(nombre_arc)
    os.startfile(nombre_arc)
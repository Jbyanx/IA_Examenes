import pandas as pd
import numpy as np


def cargar_datos(ruta_excel):
    print(f"Cargando datos desde {ruta_excel}...")

    # 1. Leer las pestañas con los nombres exactos
    df_examenes = pd.read_excel(ruta_excel, sheet_name='Examenes')
    df_franjas = pd.read_excel(ruta_excel, sheet_name='Franjas')
    df_aulas = pd.read_excel(ruta_excel, sheet_name='Aulas')
    df_matriculas = pd.read_excel(ruta_excel, sheet_name='Matriculas')

    # 2. Extraer la lista de exámenes usando la columna 'Examen'
    lista_examenes = df_examenes['Examen'].dropna().tolist()

    # Crear un diccionario para asignar a cada examen un índice de 0 a N-1
    # Ejemplo: {'E01': 0, 'E02': 1, ...}
    exam_to_idx = {}
    for i, ex in enumerate(lista_examenes):
        exam_to_idx[str(ex).strip()] = i

    num_examenes = len(exam_to_idx)

    # 3. Crear la matriz de conflictos (llena de ceros)
    matriz_conflictos = np.zeros((num_examenes, num_examenes), dtype=int)

    # 4. Agrupar matrículas por estudiante
    estudiantes_agrupados = df_matriculas.groupby('Estudiante')['Examen'].apply(list)

    # Llenar la matriz sumando los cruces
    for examenes in estudiantes_agrupados:
        # Convertimos los nombres ('E01') a sus índices matemáticos (0)
        indices = [exam_to_idx[str(e).strip()] for e in examenes if str(e).strip() in exam_to_idx]

        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                ex1 = indices[i]
                ex2 = indices[j]
                matriz_conflictos[ex1][ex2] += 1
                matriz_conflictos[ex2][ex1] += 1  # Es simétrica

    # 5. Diccionario rápido para saber qué día es cada franja (Ej: 'F1' -> 'Lunes')
    franja_a_dia = dict(zip(df_franjas['Franja'].str.strip(), df_franjas['Dia'].str.strip()))

    print("Datos vectorizados con éxito.")

    return {
        'num_examenes': num_examenes,
        'matriz_conflictos': matriz_conflictos,
        'franja_a_dia': franja_a_dia,
        'aulas': df_aulas.to_dict('records'),
        'examenes_crudos': df_examenes
    }
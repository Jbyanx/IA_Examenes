def calcular_costo(asignacion, datos):
    """
    'asignacion' es una lista de diccionarios.
    El índice de la lista corresponde al índice del examen.
    Ejemplo de un elemento: asignacion[0] = {'franja': 'F1', 'aula': 'A101', 'inscritos': 17, 'capacidad_aula': 20}
    """
    H = 0  # Violaciones de restricciones duras
    C_dia = 0  # Sobrecarga diaria
    P_libres = 0  # Asientos libres

    matriz_conflictos = datos['matriz_conflictos']
    num_examenes = datos['num_examenes']
    franja_a_dia = datos['franja_a_dia']

    # 1. Analizar los cruces entre todos los pares de exámenes
    for i in range(num_examenes):
        for j in range(i + 1, num_examenes):

            # Si dos exámenes se programan exactamente a la misma hora (Misma Franja)
            if asignacion[i]['franja'] == asignacion[j]['franja']:
                # Penalidad dura: estudiantes que ven ambos al mismo tiempo
                H += matriz_conflictos[i][j]

                # Penalidad dura: no pueden compartir la misma aula al mismo tiempo
                if asignacion[i]['aula'] == asignacion[j]['aula']:
                    H += 1

                    # Si no están a la misma hora, revisamos si cayeron el mismo día (Criterio Blando)
            else:
                dia_i = franja_a_dia.get(asignacion[i]['franja'])
                dia_j = franja_a_dia.get(asignacion[j]['franja'])

                if dia_i == dia_j:
                    C_dia += matriz_conflictos[i][j]

    # 2. Analizar las restricciones individuales por examen (Capacidad)
    for i in range(num_examenes):
        # Si hay más estudiantes que sillas en el aula asignada
        if asignacion[i]['inscritos'] > asignacion[i]['capacidad_aula']:
            H += 1
        else:
            # Sumamos las sillas sobrantes (Capacidad - Estudiantes)
            P_libres += (asignacion[i]['capacidad_aula'] - asignacion[i]['inscritos'])

    # 3. Función objetivo global con los pesos de la guía
    costo_total = (100000 * H) + (100 * C_dia) + P_libres

    return costo_total
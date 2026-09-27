import numpy as np
import random
import copy
from objective_function import calcular_costo

def generar_solucion_inicial(datos):
    """Crea un horario inicial inteligente priorizando los exámenes más conflictivos (Largest Degree)."""
    num_examenes = datos['num_examenes']
    aulas = datos['aulas']
    examenes_crudos = datos['examenes_crudos']
    matriz_conflictos = datos['matriz_conflictos']

    # 1. Sumamos la fila de cada examen para saber cuántos conflictos totales tiene
    conflictos_totales = np.sum(matriz_conflictos, axis=1)

    # 2. Ordenamos los exámenes del más conflictivo al menos conflictivo
    orden_examenes = np.argsort(-conflictos_totales)

    # Preparamos una lista vacía del tamaño correcto
    asignacion = [{}] * num_examenes

    # 3. Asignamos en el orden inteligente
    for i in orden_examenes:
        aula_elegida = random.choice(aulas)
        franjas_aula = [f.strip() for f in str(aula_elegida['Franjas_disponibles']).split(',')]
        franja_elegida = random.choice(franjas_aula)
        inscritos = examenes_crudos.iloc[i]['Estudiantes']

        asignacion[i] = {
            'franja': franja_elegida,
            'aula': aula_elegida['Aula'],
            'inscritos': inscritos,
            'capacidad_aula': aula_elegida['Capacidad']
        }

    return asignacion

def generar_vecino(asignacion, datos):
    """Operador de vecindario: Toma un examen al azar y lo cambia de aula/hora."""
    vecino = copy.deepcopy(asignacion)
    idx_examen = random.randint(0, datos['num_examenes'] - 1)

    # Le asignamos una nueva aula y franja al azar
    aula_nueva = random.choice(datos['aulas'])
    franjas_aula = [f.strip() for f in str(aula_nueva['Franjas_disponibles']).split(',')]
    franja_nueva = random.choice(franjas_aula)

    vecino[idx_examen]['aula'] = aula_nueva['Aula']
    vecino[idx_examen]['franja'] = franja_nueva
    vecino[idx_examen]['capacidad_aula'] = aula_nueva['Capacidad']

    return vecino

def ejecutar_sa(datos, parametros):
    """Motor principal del Enfriamiento Simulado."""
    T = parametros['T_inicial']
    alpha = parametros['alpha']
    iteraciones = parametros['iteraciones_por_T']
    T_final = parametros['T_final']

    # 1. Punto de partida (Ahora es Inteligente)
    solucion_actual = generar_solucion_inicial(datos)
    costo_actual = calcular_costo(solucion_actual, datos)

    mejor_solucion = copy.deepcopy(solucion_actual)
    mejor_costo = costo_actual

    # 2. Bucle de enfriamiento
    while T > T_final:
        for _ in range(iteraciones):
            vecino = generar_vecino(solucion_actual, datos)
            costo_vecino = calcular_costo(vecino, datos)

            delta = costo_vecino - costo_actual

            if delta < 0 or random.random() < np.exp(-delta / T):
                solucion_actual = vecino
                costo_actual = costo_vecino

                if costo_actual < mejor_costo:
                    mejor_solucion = copy.deepcopy(solucion_actual)
                    mejor_costo = costo_actual

        T *= alpha

    return mejor_costo, mejor_solucion
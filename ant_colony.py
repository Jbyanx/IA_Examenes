import numpy as np
import random
from objective_function import calcular_costo


def inicializar_feromonas(datos, tau_inicial):
    """Crea el mapa de rastros químicos para todas las combinaciones de (examen, aula, franja)."""
    feromonas = {}
    aulas = datos['aulas']
    for i in range(datos['num_examenes']):
        for aula in aulas:
            franjas = [f.strip() for f in str(aula['Franjas_disponibles']).split(',')]
            for franja in franjas:
                # Cada combinación inicia con el nivel máximo de feromona
                feromonas[(i, aula['Aula'], franja)] = tau_inicial
    return feromonas


def construir_solucion(datos, feromonas, alpha, beta):
    """Una hormiga construye un horario guiándose por feromonas y la heurística."""
    asignacion = []
    aulas = datos['aulas']
    examenes_crudos = datos['examenes_crudos']

    for i in range(datos['num_examenes']):
        opciones = []
        probabilidades = []
        inscritos = examenes_crudos.iloc[i]['Estudiantes']

        # Evaluar qué tan atractiva es cada opción (aula, franja) para este examen
        for aula in aulas:
            franjas = [f.strip() for f in str(aula['Franjas_disponibles']).split(',')]
            for franja in franjas:
                tau = feromonas[(i, aula['Aula'], franja)]

                # Información heurística (eta): preferimos aulas donde quepan los alumnos
                eta = 2.0 if aula['Capacidad'] >= inscritos else 0.1

                # Fórmula de probabilidad de transición del ACO
                peso = (tau ** alpha) * (eta ** beta)

                opciones.append({
                    'franja': franja,
                    'aula': aula['Aula'],
                    'inscritos': inscritos,
                    'capacidad_aula': aula['Capacidad']
                })
                probabilidades.append(peso)

        # Convertir pesos en probabilidades (Ruleta)
        suma_prob = sum(probabilidades)
        probabilidades = [p / suma_prob for p in probabilidades]

        # La hormiga toma la decisión probabilística usando numpy
        idx_elegido = np.random.choice(len(opciones), p=probabilidades)
        asignacion.append(opciones[idx_elegido])

    return asignacion


def ejecutar_aco(datos, parametros):
    """Motor principal de la Optimización por Colonias de Hormigas (MMAS)."""
    num_hormigas = parametros['num_hormigas']
    iteraciones = parametros['iteraciones']
    alpha = parametros['alpha']
    beta = parametros['beta']
    rho = parametros['evaporacion']
    tau_max = parametros['tau_max']
    tau_min = parametros['tau_min']

    # 1. Inicialización
    feromonas = inicializar_feromonas(datos, tau_max)

    mejor_solucion_global = None
    mejor_costo_global = float('inf')

    # 2. Bucle principal de iteraciones (generaciones de hormigas)
    for _ in range(iteraciones):

        # Fase constructiva: el enjambre crea las soluciones
        for h in range(num_hormigas):
            solucion = construir_solucion(datos, feromonas, alpha, beta)
            costo = calcular_costo(solucion, datos)

            # Si esta hormiga encontró la mejor solución histórica, la guardamos
            if costo < mejor_costo_global:
                mejor_costo_global = costo
                mejor_solucion_global = solucion

        # Fase de evaporación: el rastro químico se va secando
        for key in feromonas:
            feromonas[key] = feromonas[key] * (1 - rho)
            if feromonas[key] < tau_min:  # Límite inferior MMAS
                feromonas[key] = tau_min

        # Fase de refuerzo (Elitismo global): solo la mejor hormiga histórica deposita feromona
        aporte = 100000.0 / (mejor_costo_global + 1)
        for i, asignacion in enumerate(mejor_solucion_global):
            key = (i, asignacion['aula'], asignacion['franja'])
            feromonas[key] += aporte
            if feromonas[key] > tau_max:  # Límite superior MMAS
                feromonas[key] = tau_max

    return mejor_costo_global, mejor_solucion_global
import concurrent.futures
import numpy as np
import random
import time
import pandas as pd
from data_loader import cargar_datos
from simulated_annealing import ejecutar_sa
from ant_colony import ejecutar_aco


def tarea_simulacion(semilla):
    """
    Esta función es lo que correrá cada núcleo de tu procesador.
    """
    inicio_tarea = time.time()  # Empezamos a cronometrar este hilo

    # Fijar la semilla para cumplir el requisito de 'Reproducibilidad'
    np.random.seed(semilla)
    random.seed(semilla)

    # Parámetros básicos para la Línea Base del experimento
    parametros_sa = {
        'T_inicial': 10000.0,
        'alpha': 0.95,
        'iteraciones_por_T': 100,
        'T_final': 1.0
    }

    # Parámetros básicos para la Línea Base del ACO (MAX-MIN Ant System)
    parametros_aco = {
        'num_hormigas': 10,
        'iteraciones': 20,
        'alpha': 1.0,  # Peso de la feromona
        'beta': 2.0,  # Peso de la heurística
        'evaporacion': 0.1,  # Tasa de olvido (rho)
        'tau_max': 10.0,
        'tau_min': 0.1
    }

    # Ejecutamos el algoritmo ACO
    costo_final, mejor_horario = ejecutar_aco(datos_globales, parametros_aco)

    # Ejecutamos el algoritmo real
    costo_final, mejor_horario = ejecutar_sa(datos_globales, parametros_sa)

    fin_tarea = time.time()  # Terminamos de cronometrar
    tiempo_ejecucion = fin_tarea - inicio_tarea

    # Ahora retornamos también el tiempo que tardó
    return {
        'semilla': semilla,
        'costo': costo_final,
        'tiempo_segundos': round(tiempo_ejecucion, 2)
    }


if __name__ == '__main__':
    nombre_archivo = 'instancia_examenes_tema03.xlsx'

    try:
        print("--- INICIANDO SISTEMA DE ASIGNACIÓN ---")
        datos_globales = cargar_datos(nombre_archivo)

        print("\nDesplegando 30 ejecuciones en paralelo...")
        semillas = list(range(1, 31))
        resultados = []

        inicio_tiempo = time.time()

        # Lanzamos el multiprocesamiento
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for resultado in executor.map(tarea_simulacion, semillas):
                resultados.append(resultado)
                print(
                    f"Completado: Semilla {resultado['semilla']} -> Costo: {resultado['costo']} (Tiempo: {resultado['tiempo_segundos']}s)")

        # ¡ATENCIÓN! Todo este bloque ahora está afuera del 'with' y del 'for'
        fin_tiempo = time.time()
        print(f"\n¡Las 30 simulaciones terminaron en {fin_tiempo - inicio_tiempo:.2f} segundos!")

        nombre_base = 'resultados_ACO_linea_base'

        df_resultados = pd.DataFrame(resultados)

        tiempo_total_suma = df_resultados['tiempo_segundos'].sum()
        fila_total = pd.DataFrame([{
            'semilla': 'TOTAL',
            'costo': '',
            'tiempo_segundos': round(tiempo_total_suma, 2)
        }])

        df_resultados = pd.concat([df_resultados, fila_total], ignore_index=True)
        df_resultados.to_csv(f'{nombre_base}.csv', index=False)

        nota_explicativa = """Algoritmo: Optimización por Colonias de Hormigas (MMAS - MAX-MIN Ant System)
        Experimento: Línea Base (Baseline).
        Parámetros: num_hormigas=10, iteraciones=20, alpha=1.0, beta=2.0, evaporacion=0.1.
        Comportamiento: Se evalúa la convergencia del algoritmo usando una influencia heurística moderada y límites de feromona.
        """

        with open(f'{nombre_base}.txt', 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write(nota_explicativa)

        print(f"¡Resultados guardados en '{nombre_base}.csv' y '{nombre_base}.txt'!")

    except FileNotFoundError:
        print(
            f"Error: No se encontró el archivo '{nombre_archivo}'. Asegúrate de haberlo pegado en la misma carpeta que este script.")
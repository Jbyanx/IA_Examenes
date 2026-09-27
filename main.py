import concurrent.futures
import numpy as np
import random
import time
import pandas as pd
from ant_colony import ejecutar_aco
from data_loader import cargar_datos


def tarea_simulacion_aco(semilla, parametros_aco):
    inicio_tarea = time.time()
    np.random.seed(semilla)
    random.seed(semilla)

    # Ejecutamos el algoritmo de Hormigas
    costo_final, mejor_horario = ejecutar_aco(datos_globales, parametros_aco)

    fin_tarea = time.time()
    tiempo_ejecucion = fin_tarea - inicio_tarea

    return {
        'semilla': semilla,
        'costo': costo_final,
        'tiempo_segundos': round(tiempo_ejecucion, 2)
    }


if __name__ == '__main__':
    nombre_archivo = 'instancia_examenes_tema03.xlsx'

    try:
        print("--- INICIANDO SISTEMA DE ASIGNACIÓN (BLOQUE 1 - ACO) ---")
        datos_globales = cargar_datos(nombre_archivo)
        semillas = list(range(1, 31))

        # Malla de 10 configuraciones exploratorias para el Bloque 1 de ACO
        configuraciones_bloque_1_aco = [
            {'id': 1, 'num_hormigas': 10, 'iteraciones': 20, 'alpha': 1.0, 'beta': 1.0, 'evaporacion': 0.1,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 2, 'num_hormigas': 10, 'iteraciones': 20, 'alpha': 1.0, 'beta': 3.0, 'evaporacion': 0.1,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 3, 'num_hormigas': 10, 'iteraciones': 20, 'alpha': 1.0, 'beta': 5.0, 'evaporacion': 0.1,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 4, 'num_hormigas': 20, 'iteraciones': 20, 'alpha': 1.0, 'beta': 3.0, 'evaporacion': 0.1,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 5, 'num_hormigas': 20, 'iteraciones': 20, 'alpha': 1.0, 'beta': 5.0, 'evaporacion': 0.1,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 6, 'num_hormigas': 10, 'iteraciones': 50, 'alpha': 1.0, 'beta': 3.0, 'evaporacion': 0.1,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 7, 'num_hormigas': 10, 'iteraciones': 50, 'alpha': 1.0, 'beta': 5.0, 'evaporacion': 0.1,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 8, 'num_hormigas': 20, 'iteraciones': 50, 'alpha': 1.0, 'beta': 3.0, 'evaporacion': 0.1,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 9, 'num_hormigas': 20, 'iteraciones': 20, 'alpha': 1.0, 'beta': 3.0, 'evaporacion': 0.3,
             'tau_max': 10.0, 'tau_min': 0.1},
            {'id': 10, 'num_hormigas': 20, 'iteraciones': 50, 'alpha': 1.0, 'beta': 3.0, 'evaporacion': 0.3,
             'tau_max': 10.0, 'tau_min': 0.1}
        ]

        nombre_bitacora = 'bitacora_ACO_Bloque1.txt'

        with open(nombre_bitacora, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write("BITÁCORA DE EXPERIMENTACIÓN - BLOQUE 1 (COLONIAS DE HORMIGAS - MMAS)\n")
            archivo_txt.write("=" * 65 + "\n\n")

        tiempo_inicio_global = time.time()

        for config in configuraciones_bloque_1_aco:
            print(f"\n--- Ejecutando Configuración {config['id']} / 10 ---")
            print(
                f"Hormigas={config['num_hormigas']}, Iter={config['iteraciones']}, Beta={config['beta']}, Rho={config['evaporacion']}")

            resultados = []
            lista_parametros = [config] * len(semillas)

            with concurrent.futures.ProcessPoolExecutor() as executor:
                for resultado in executor.map(tarea_simulacion_aco, semillas, lista_parametros):
                    resultados.append(resultado)

            nombre_csv = f"resultados_ACO_Bloque1_Config_{config['id']}.csv"
            df_resultados = pd.DataFrame(resultados)

            tiempo_total_suma = df_resultados['tiempo_segundos'].sum()
            fila_total = pd.DataFrame(
                [{'semilla': 'TOTAL', 'costo': '', 'tiempo_segundos': round(tiempo_total_suma, 2)}])

            df_resultados = pd.concat([df_resultados, fila_total], ignore_index=True)
            df_resultados.to_csv(nombre_csv, index=False)

            with open(nombre_bitacora, 'a', encoding='utf-8') as archivo_txt:
                archivo_txt.write(f"Configuración {config['id']}:\n")
                archivo_txt.write(f"- Archivo: {nombre_csv}\n")
                archivo_txt.write(f"- num_hormigas: {config['num_hormigas']}\n")
                archivo_txt.write(f"- iteraciones: {config['iteraciones']}\n")
                archivo_txt.write(f"- beta (heurística): {config['beta']}\n")
                archivo_txt.write(f"- evaporacion (rho): {config['evaporacion']}\n")
                archivo_txt.write(f"- Tiempo de procesamiento CPU (suma total): {round(tiempo_total_suma, 2)} s\n")
                archivo_txt.write("-" * 40 + "\n")

            print(f"Configuración {config['id']} completada y guardada en {nombre_csv}")

        tiempo_fin_global = time.time()
        print(
            f"\n¡EL BLOQUE 1 ACO COMPLETADO! Tiempo total en la vida real: {round((tiempo_fin_global - tiempo_inicio_global) / 60, 2)} minutos.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
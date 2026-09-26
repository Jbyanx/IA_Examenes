import concurrent.futures
import numpy as np
import random
import time
import pandas as pd
from simulated_annealing import ejecutar_sa
from data_loader import cargar_datos


def tarea_simulacion(semilla, parametros_sa):
    """
    Esta función ahora recibe la semilla y los parámetros específicos de la configuración actual.
    """
    inicio_tarea = time.time()

    np.random.seed(semilla)
    random.seed(semilla)

    # Ejecutamos el algoritmo con los parámetros que nos pasaron
    costo_final, mejor_horario = ejecutar_sa(datos_globales, parametros_sa)

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
        print("--- INICIANDO SISTEMA DE ASIGNACIÓN (BLOQUE 1 - SA) ---")
        datos_globales = cargar_datos(nombre_archivo)
        semillas = list(range(1, 31))

        # Malla de 10 configuraciones experimentales para el Bloque 1
        configuraciones_bloque_1 = [
            {'id': 1, 'T_inicial': 5000.0, 'alpha': 0.90, 'iteraciones_por_T': 50, 'T_final': 1.0},
            {'id': 2, 'T_inicial': 5000.0, 'alpha': 0.95, 'iteraciones_por_T': 50, 'T_final': 1.0},
            {'id': 3, 'T_inicial': 5000.0, 'alpha': 0.99, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 4, 'T_inicial': 10000.0, 'alpha': 0.90, 'iteraciones_por_T': 50, 'T_final': 1.0},
            {'id': 5, 'T_inicial': 10000.0, 'alpha': 0.95, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 6, 'T_inicial': 10000.0, 'alpha': 0.99, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 7, 'T_inicial': 20000.0, 'alpha': 0.85, 'iteraciones_por_T': 150, 'T_final': 1.0},
            {'id': 8, 'T_inicial': 20000.0, 'alpha': 0.90, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 9, 'T_inicial': 20000.0, 'alpha': 0.95, 'iteraciones_por_T': 150, 'T_final': 1.0},
            {'id': 10, 'T_inicial': 20000.0, 'alpha': 0.99, 'iteraciones_por_T': 50, 'T_final': 1.0}
        ]

        nombre_bitacora = 'bitacora_SA_Bloque1.txt'

        # Creamos/limpiamos el archivo de bitácora antes de empezar
        with open(nombre_bitacora, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write("BITÁCORA DE EXPERIMENTACIÓN - BLOQUE 1 (ENFRIAMIENTO SIMULADO)\n")
            archivo_txt.write("=" * 65 + "\n\n")

        tiempo_inicio_global = time.time()

        # Iteramos sobre las 10 configuraciones
        for config in configuraciones_bloque_1:
            print(f"\n--- Ejecutando Configuración {config['id']} / 10 ---")
            print(f"Parámetros: T={config['T_inicial']}, alpha={config['alpha']}, iter={config['iteraciones_por_T']}")

            resultados = []

            # Repetimos la lista de parámetros 30 veces para que el map la reciba correctamente
            lista_parametros = [config] * len(semillas)

            # Lanzamos el multiprocesamiento para esta configuración específica
            with concurrent.futures.ProcessPoolExecutor() as executor:
                for resultado in executor.map(tarea_simulacion, semillas, lista_parametros):
                    resultados.append(resultado)

            # Guardado del CSV para esta configuración
            nombre_csv = f"resultados_SA_Bloque1_Config_{config['id']}.csv"
            df_resultados = pd.DataFrame(resultados)

            tiempo_total_suma = df_resultados['tiempo_segundos'].sum()
            fila_total = pd.DataFrame(
                [{'semilla': 'TOTAL', 'costo': '', 'tiempo_segundos': round(tiempo_total_suma, 2)}])

            df_resultados = pd.concat([df_resultados, fila_total], ignore_index=True)
            df_resultados.to_csv(nombre_csv, index=False)

            # Escribir los detalles en la bitácora general
            with open(nombre_bitacora, 'a', encoding='utf-8') as archivo_txt:
                archivo_txt.write(f"Configuración {config['id']}:\n")
                archivo_txt.write(f"- Archivo: {nombre_csv}\n")
                archivo_txt.write(f"- T_inicial: {config['T_inicial']}\n")
                archivo_txt.write(f"- alpha (tasa de enfriamiento): {config['alpha']}\n")
                archivo_txt.write(f"- iteraciones_por_T: {config['iteraciones_por_T']}\n")
                archivo_txt.write(f"- Tiempo de procesamiento CPU (suma total): {round(tiempo_total_suma, 2)} s\n")
                archivo_txt.write("-" * 40 + "\n")

            print(f"Configuración {config['id']} completada y guardada en {nombre_csv}")

        tiempo_fin_global = time.time()
        print(
            f"\n¡EL BLOQUE 1 COMPLETADO! Tiempo total en la vida real: {round((tiempo_fin_global - tiempo_inicio_global) / 60, 2)} minutos.")
        print(
            f"Revisa tu carpeta, tienes 10 archivos CSV nuevos y tu archivo de bitácora '{nombre_bitacora}' documentando todo.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
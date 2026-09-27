import concurrent.futures
import numpy as np
import random
import time
import pandas as pd
from simulated_annealing import ejecutar_sa
from data_loader import cargar_datos


def tarea_simulacion(semilla, parametros_sa):
    inicio_tarea = time.time()
    np.random.seed(semilla)
    random.seed(semilla)

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
        print("--- INICIANDO SISTEMA DE ASIGNACIÓN (BLOQUE 2 - SA REFINADO) ---")
        datos_globales = cargar_datos(nombre_archivo)
        semillas = list(range(1, 31))

        # Malla de 10 configuraciones REFINADAS para el Bloque 2
        # Nos enfocamos en alphas altos y heurística inteligente activada
        configuraciones_bloque_2 = [
            {'id': 1, 'T_inicial': 5000.0, 'alpha': 0.96, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 2, 'T_inicial': 5000.0, 'alpha': 0.98, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 3, 'T_inicial': 5000.0, 'alpha': 0.99, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 4, 'T_inicial': 10000.0, 'alpha': 0.96, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 5, 'T_inicial': 10000.0, 'alpha': 0.98, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 6, 'T_inicial': 10000.0, 'alpha': 0.99, 'iteraciones_por_T': 100, 'T_final': 1.0},
            {'id': 7, 'T_inicial': 10000.0, 'alpha': 0.99, 'iteraciones_por_T': 150, 'T_final': 1.0},
            {'id': 8, 'T_inicial': 10000.0, 'alpha': 0.97, 'iteraciones_por_T': 120, 'T_final': 1.0},
            {'id': 9, 'T_inicial': 5000.0, 'alpha': 0.99, 'iteraciones_por_T': 150, 'T_final': 1.0},
            {'id': 10, 'T_inicial': 5000.0, 'alpha': 0.97, 'iteraciones_por_T': 120, 'T_final': 1.0}
        ]

        nombre_bitacora = 'bitacora_SA_Bloque2.txt'

        with open(nombre_bitacora, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write("BITÁCORA DE EXPERIMENTACIÓN - BLOQUE 2 (ENFRIAMIENTO SIMULADO REFINADO)\n")
            archivo_txt.write("=" * 65 + "\n\n")

        tiempo_inicio_global = time.time()

        for config in configuraciones_bloque_2:
            print(f"\n--- Ejecutando Configuración {config['id']} / 10 ---")
            print(f"Parámetros: T={config['T_inicial']}, alpha={config['alpha']}, iter={config['iteraciones_por_T']}")

            resultados = []
            lista_parametros = [config] * len(semillas)

            with concurrent.futures.ProcessPoolExecutor() as executor:
                for resultado in executor.map(tarea_simulacion, semillas, lista_parametros):
                    resultados.append(resultado)

            nombre_csv = f"resultados_SA_Bloque2_Config_{config['id']}.csv"
            df_resultados = pd.DataFrame(resultados)

            tiempo_total_suma = df_resultados['tiempo_segundos'].sum()
            fila_total = pd.DataFrame(
                [{'semilla': 'TOTAL', 'costo': '', 'tiempo_segundos': round(tiempo_total_suma, 2)}])

            df_resultados = pd.concat([df_resultados, fila_total], ignore_index=True)
            df_resultados.to_csv(nombre_csv, index=False)

            with open(nombre_bitacora, 'a', encoding='utf-8') as archivo_txt:
                archivo_txt.write(f"Configuración {config['id']}:\n")
                archivo_txt.write(f"- Archivo: {nombre_csv}\n")
                archivo_txt.write(f"- T_inicial: {config['T_inicial']}\n")
                archivo_txt.write(f"- alpha (tasa de enfriamiento): {config['alpha']}\n")
                archivo_txt.write(f"- iteraciones_por_T: {config['iteraciones_por_T']}\n")
                archivo_txt.write(f"- Heurística Inicial: ACTIVADA (Largest Degree)\n")
                archivo_txt.write(f"- Tiempo de procesamiento CPU (suma total): {round(tiempo_total_suma, 2)} s\n")
                archivo_txt.write("-" * 40 + "\n")

            print(f"Configuración {config['id']} completada y guardada en {nombre_csv}")

        tiempo_fin_global = time.time()
        print(
            f"\n¡EL BLOQUE 2 COMPLETADO! Tiempo total en la vida real: {round((tiempo_fin_global - tiempo_inicio_global) / 60, 2)} minutos.")
        print(
            f"Revisa tu carpeta, tienes 10 archivos CSV nuevos y tu archivo de bitácora '{nombre_bitacora}' documentando todo.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
import concurrent.futures
import numpy as np
import random
import time
import pandas as pd
from simulated_annealing import ejecutar_sa
from ant_colony import ejecutar_aco
from data_loader import cargar_datos


def tarea_validacion_sa(semilla, parametros):
    inicio = time.time()
    np.random.seed(semilla)
    random.seed(semilla)
    costo, _ = ejecutar_sa(datos_globales, parametros)
    return {'semilla': semilla, 'costo': costo, 'tiempo_segundos': round(time.time() - inicio, 2)}


def tarea_validacion_aco(semilla, parametros):
    inicio = time.time()
    np.random.seed(semilla)
    random.seed(semilla)
    costo, _ = ejecutar_aco(datos_globales, parametros)
    return {'semilla': semilla, 'costo': costo, 'tiempo_segundos': round(time.time() - inicio, 2)}


if __name__ == '__main__':
    nombre_archivo = 'instancia_examenes_tema03.xlsx'

    try:
        print("--- INICIANDO VALIDACIÓN FINAL (SA vs ACO) ---")
        datos_globales = cargar_datos(nombre_archivo)

        # SEMILLAS NUEVAS PARA VALIDACIÓN (31 al 60)
        semillas_validacion = list(range(31, 61))

        # Parámetros de los Campeones
        parametros_campeon_sa = {'T_inicial': 5000.0, 'alpha': 0.97, 'iteraciones_por_T': 120, 'T_final': 1.0}
        parametros_campeon_aco = {'num_hormigas': 50, 'iteraciones': 100, 'alpha': 1.0, 'beta': 5.0, 'evaporacion': 0.5,
                                  'tau_max': 10.0, 'tau_min': 0.1}

        # ---------------------------------------------------------
        # 1. EJECUTAR EL CAMPEÓN SA
        # ---------------------------------------------------------
        print("\n[1/2] Ejecutando Campeón SA en nuevas semillas...")
        resultados_sa = []
        lista_params_sa = [parametros_campeon_sa] * len(semillas_validacion)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for res in executor.map(tarea_validacion_sa, semillas_validacion, lista_params_sa):
                resultados_sa.append(res)

        df_sa = pd.DataFrame(resultados_sa)
        df_sa.to_csv("resultados_Validacion_SA_Campeon.csv", index=False)
        print("-> Campeón SA completado.")

        # ---------------------------------------------------------
        # 2. EJECUTAR EL CAMPEÓN ACO
        # ---------------------------------------------------------
        print("\n[2/2] Ejecutando Campeón ACO en nuevas semillas...")
        resultados_aco = []
        lista_params_aco = [parametros_campeon_aco] * len(semillas_validacion)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for res in executor.map(tarea_validacion_aco, semillas_validacion, lista_params_aco):
                resultados_aco.append(res)

        df_aco = pd.DataFrame(resultados_aco)
        df_aco.to_csv("resultados_Validacion_ACO_Campeon.csv", index=False)
        print("-> Campeón ACO completado.")

        print("\n¡VALIDACIÓN FINAL COMPLETADA CON ÉXITO!")
        print(
            "Se generaron los archivos 'resultados_Validacion_SA_Campeon.csv' y 'resultados_Validacion_ACO_Campeon.csv'")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
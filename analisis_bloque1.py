import pandas as pd

resultados_analisis = []

# Iteramos sobre los 10 archivos que generamos
for i in range(1, 11):
    nombre_archivo = f'resultados/5.resultados_SA_Bloque2/resultados_SA_Bloque2_Config_{i}.csv'
    try:
        df = pd.read_csv(nombre_archivo)

        # Filtramos la fila de "TOTAL" para que no altere las matemáticas
        df_limpio = df[df['semilla'] != 'TOTAL'].copy()

        # Aseguramos que la columna costo se lea como número
        df_limpio['costo'] = pd.to_numeric(df_limpio['costo'])

        # Cálculos estadísticos clave
        costo_promedio = df_limpio['costo'].mean()
        mejor_costo = df_limpio['costo'].min()
        desviacion_estandar = df_limpio['costo'].std()

        # Coeficiente de Variación (CV) en porcentaje
        cv = (desviacion_estandar / costo_promedio) * 100 if costo_promedio > 0 else 0

        # Tiempo promedio por semilla
        df_limpio['tiempo_segundos'] = pd.to_numeric(df_limpio['tiempo_segundos'])
        tiempo_promedio = df_limpio['tiempo_segundos'].mean()

        resultados_analisis.append({
            'Config': f"Config {i}",
            'Promedio': round(costo_promedio, 2),
            'Mejor Costo': mejor_costo,
            'CV (%)': round(cv, 2),
            'Tiempo Prom (s)': round(tiempo_promedio, 2)
        })
    except FileNotFoundError:
        print(f"Advertencia: No se encontró {nombre_archivo}")

# Convertimos los resultados en un DataFrame para ordenarlo y mostrarlo
df_ranking = pd.DataFrame(resultados_analisis)

# Ordenamos del mejor promedio al peor
df_ranking = df_ranking.sort_values(by='Promedio')

print("\n--- RANKING FINAL DEL BLOQUE 1 (ENFRIAMIENTO SIMULADO) ---")
print(df_ranking.to_string(index=False))
print("-" * 65)
print("NOTA: Busca la configuración con el menor 'Promedio' y un 'CV (%)' bajo (menor al 5-10%).")
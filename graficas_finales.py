import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generar_reporte_y_graficas():
    print("Generando análisis final y gráficas...")

    # 1. Leer los archivos de validación
    try:
        df_sa = pd.read_csv('resultados_Validacion_SA_Campeon.csv')
        df_aco = pd.read_csv('resultados_Validacion_ACO_Campeon.csv')
    except FileNotFoundError:
        print("Error: No se encontraron los archivos CSV de validación.")
        return

    # 2. Calcular la tabla estadística
    resultados = []
    for nombre, df in [('Enfriamiento Simulado (SA)', df_sa), ('Colonias de Hormigas (ACO)', df_aco)]:
        promedio = df['costo'].mean()
        mejor = df['costo'].min()
        peor = df['costo'].max()
        std = df['costo'].std()
        cv = (std / promedio) * 100
        tiempo_prom = df['tiempo_segundos'].mean()

        resultados.append({
            'Algoritmo': nombre,
            'Costo Promedio': round(promedio, 2),
            'Mejor Costo': mejor,
            'Peor Costo': peor,
            'CV (%)': round(cv, 2),
            'Tiempo Prom (s)': round(tiempo_prom, 2)
        })

    df_resumen = pd.DataFrame(resultados)

    print("\n" + "=" * 70)
    print("TABLA ESTADÍSTICA OFICIAL PARA LA PRESENTACIÓN")
    print("=" * 70)
    print(df_resumen.to_string(index=False))
    print("=" * 70 + "\n")

    # 3. Generar el Boxplot Comparativo
    # Unimos los datos para graficarlos juntos
    df_sa['Algoritmo'] = 'SA (Campeón)'
    df_aco['Algoritmo'] = 'ACO (Campeón)'
    df_total = pd.concat([df_sa, df_aco])

    # Configuramos el estilo de la gráfica
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Creamos el boxplot
    ax = sns.boxplot(x='Algoritmo', y='costo', data=df_total, palette="Set2")

    # ¡CLAVE! Usamos escala logarítmica porque el ACO está en millones y el SA llega a miles
    plt.yscale('log')

    plt.title('Dispersión de Costos: Enfriamiento Simulado vs Colonias de Hormigas', fontsize=16)
    plt.ylabel('Costo de la Solución (Escala Logarítmica)', fontsize=12)
    plt.xlabel('Metaheurística', fontsize=12)

    # Guardamos la imagen en alta calidad
    nombre_imagen = 'boxplot_validacion_final.png'
    plt.savefig(nombre_imagen, dpi=300, bbox_inches='tight')
    print(f"¡Gráfica exportada exitosamente como '{nombre_imagen}'!")


if __name__ == '__main__':
    generar_reporte_y_graficas()
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

def pie_graph_towns(madera_plastica_percent, materia_prima_percent, productos_inyeccion_percent, otros_percent, path_to_save):
    """
    Función para crear un gráfico de pastel con los porcentajes de distribución de
    cuatro categorías: madera plástica, materia prima, productos de inyección y otros.

    Args:
    - madera_plastica_percent (float): Porcentaje de madera plástica.
    - materia_prima_percent (float): Porcentaje de materia prima.
    - productos_inyeccion_percent (float): Porcentaje de productos de inyección.
    - otros_percent (float): Porcentaje de otros.
    - path_to_save (str): Ruta donde se guardará el gráfico.

    Si todos los valores son cero, se configura cada categoría al 25% y se establece
    una etiqueta numérica personalizada de '0%' para todas las categorías.
    """

    # Verificar si todos los valores son cero
    if madera_plastica_percent == materia_prima_percent == productos_inyeccion_percent == otros_percent == 0:
        sizes = [25, 25, 25, 25]  # Establecer cada categoría al 25%
        autopct_labels = ['0%']  # Solo una etiqueta de '0%'
    else:
        sizes = [madera_plastica_percent, materia_prima_percent, productos_inyeccion_percent, otros_percent]
        autopct_labels = '%1.0f%%'  # Formato de porcentaje para valores no cero

    labels = ['Madera plástica', 'Productos de inyección', 'Materia prima', 'Otros']
    colors = ['#78C505', '#C1FF72', '#7ED957', '#00BF63']

    # Crear una figura y un conjunto de subgráficos
    fig, ax = plt.subplots()

    # Gráfico de pastel
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct=lambda pct: autopct_labels[0] if isinstance(autopct_labels, list) else autopct_labels % pct,
        startangle=90,
        pctdistance=0.75
    )

    # Configuraciones de texto
    plt.setp(autotexts, size=15, color="black")
    plt.setp(texts, size=15, color="black")

    # Igualar aspecto para que se dibuje como un círculo
    ax.axis('equal')  

    # Ajustes de posición y título
    ax.set_position([0.1, 0.1, 0.75, 0.75])
    plt.title(' ', pad=20)
    plt.tight_layout()

    # Guardar el gráfico
    plt.savefig(path_to_save, transparent=False, bbox_inches='tight', pad_inches=0)

# Ejemplo de cómo llamar a la función
pie_graph_towns(
   30, 10, 10, 25,
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "images_for_report/img_type_of_products_towns.png")
)

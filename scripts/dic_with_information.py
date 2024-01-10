# Connection to the database
from pymongo import MongoClient
import os

def extract_and_transform_data():
    """
    Extract and transform data from MongoDB.

    Returns:
    - List of flattened dictionaries containing the data from the MongoDB collection.
    """
    # URI of the database on Atlas
    uri = os.environ.get('data_clickgreen')

    # Establish the connection with the database
    client = MongoClient(uri)

    # Access the desired database and collection
    db = client['Reports']
    collection = db['monthly_gv']
    # Retrieve all documents from the collection
    documentos = list(collection.find())

    # Flatten the dictionaries
    def flatten_dict_list(dict_list):
        """
        Flatten a list of dictionaries.

        Args:
        - dict_list: List of dictionaries to flatten.

        Returns:
        - List of flattened dictionaries.
        """
        result_list = []

        def flatten(dictionary, prefix=""):
            """
            Flatten a nested dictionary.

            Args:
            - dictionary: The dictionary to flatten.
            - prefix: Prefix for the keys in the flattened dictionary.

            Returns:
            - Flattened dictionary.
            """
            result = {}
            for key, value in dictionary.items():
                if isinstance(value, dict) and key != "Capital_del_Proyecto_en_ejecucion":
                    sub_dict = flatten(value)
                    result.update(sub_dict)
                else:
                    result[prefix + key] = value
            return result

        for dictionary in dict_list:
            result_list.append(flatten(dictionary))

        return result_list
    
    documentos = flatten_dict_list(documentos)
    return documentos

def add_additional_keys(dictionary, path_img_1, path_img_2):
    """
    Add additional keys for images to the dictionary.

    Args:
    - dictionary: The dictionary to add the keys to.
    - path_img_1: Path to the first image.
    - path_img_2: Path to the second image.

    Returns:
    - The updated dictionary with added image keys.
    """
    # Paths for images in normal reports
    path_img_cumplimiento_actual_del_proyecto = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images_for_report/img_cumplimiento_actual_del_proyecto.png")
    path_img_cumplimiento_actual_de_la_fase = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images_for_report/img_cumplimiento_actual_de_la_fase.png")
    path_img_grafica_valor_ejecutado_y_valor_restante = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images_for_report/img_valor_ejecutado_y_valor_restante.png")

    # Paths for images in Towns reports
    path_img_grafica_pie_tipo_de_productos = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images_for_report/img_type_of_products_towns.png")
    
    if dictionary['id_project'] == 'PM-SC1':
        # Update dictionary with image paths for Towns reports
        dictionary.update(
            {
                "img_principal": {
                    "path": path_img_1,
                    "width": 530,
                    "height": 530,
                    "x": 950,
                    "y": 200,
                    "page": 4
                },         
                "img_grafica_valor_ejecutado_y_valor_restante": {
                    "path": path_img_grafica_valor_ejecutado_y_valor_restante,
                    "width": 1350,
                    "height": 400,
                    "x": 160,
                    "y": 1620,
                    "page": 2
                },
                "img_grafica_pie_tipo_de_productos": {
                    "path": path_img_grafica_pie_tipo_de_productos,
                    "width": int(1.3*550),
                    "height": 550,
                    "x": 880,
                    "y": 1320,
                    "page": 3
                }
            }
        )
    else:
        # Update dictionary with image paths for normal reports
        dictionary.update({
            "img_principal": {
                "path": path_img_1,
                "width": 400,
                "height": 400,
                "x": 1110,
                "y": 320,
                "page": 2
            },
            "img_cumplimiento_actual_del_proyecto": {
                "path": path_img_cumplimiento_actual_del_proyecto,
                "width": 220,
                "height": 220,
                "x": 180,
                "y": 1810,
                "page": 2
            },
            "img_cumplimiento_actual_de_la_fase": {
                "path": path_img_cumplimiento_actual_de_la_fase,
                "width": 220,
                "height": 220,
                "x": 555,
                "y": 1810,
                "page": 2
            },
            "img_grafica_valor_ejecutado_y_valor_restante": {
                "path": path_img_grafica_valor_ejecutado_y_valor_restante,
                "width": 1350,
                "height": 400,
                "x": 180,
                "y": 460,
                "page": 3
            },
            "img_que_dice_la_empresa_posible_imagen": {
                "path": path_img_2,
                "width": 475,
                "height": 475,
                "x": 1080,
                "y": 1280,
                "page": 3
            }
        })

    return dictionary

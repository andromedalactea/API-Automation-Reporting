# Standard library imports
import io
import math
import os
import smtplib

# Third party imports
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fpdf import FPDF
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from matplotlib import font_manager
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pdf2image import convert_from_path
import pdfrw
from PIL import Image
from pymongo import MongoClient

# Local application/library specific imports
from scripts.dic_with_information import extract_and_transform_data, add_additional_keys
from scripts.history_informs import write_in_sheets, update_to_drive_pdf
from scripts.images_for_report import donut_graph, Horizontal_Bar_Graph, pie_graph_towns, download_images_of_project
from scripts.Writing_and_send_emails import get_emails_by_project_id, send_email
from scripts.write_in_pdf_and_add_images import write_in_pdf_and_add_images, images_to_pdf

#-----------------------------------------------------------------------------------------------------
# Start te logic fo the reports
def reports_for_gv(project_list, for_gv):
    """
    Generate reports for GreenVestors (GV) based on the given project list.

    Args:
    - project_list: List of project IDs to include in the report.
    - for_gv: Boolean indicating if the report is for GreenVestors.
    
    Returns:
    - A message indicating the success of the operation and the emails of GreenVestors.
    """

    # Extract report information:
    documentos = extract_and_transform_data()

    # Filter dictionaries by 'id_project' value
    documentos_filtrados = [d for d in documentos if d['id_project'] in project_list]
    for dic in documentos_filtrados:

        # Define image extensions
        extensions = [
            ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", 
            ".ico", ".jfif", ".webp", ".heif", ".indd", ".raw", ".ai", 
            ".eps", ".pdf", ".svg"
        ]

        # Remove previous images and find corresponding paths
        dir_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images_for_report")
        file_names = ['1', '2']
        for file_name in file_names:
            for ext in extensions:
                path = os.path.join(dir_name, file_name + ext)
                if os.path.isfile(path):
                    os.remove(path)
                    break

        # Download images from the Drive folder
        download_images_of_project(dic['images'])

        # Find the path of the downloaded images and add to the dictionary
        for file_name in file_names:
            for ext in extensions:
                path = os.path.join(dir_name, file_name + ext)
                if os.path.isfile(path):
                    dic['path_' + file_name] = path
                    break

        # Different flow depending on whether the report is for towns or other projects
        if dic['id_project'] == 'PM-SC1':
            # Data for the project's capital bar graph
            capital_data = dic['Capital_del_Proyecto_en_ejecucion']
            Valor_restante_para_ejecucion = capital_data['Valor_restante_para_ejecucion']
            Valor_ejecutado_a_la_fecha = capital_data['Valor_ejecutado_a_la_fecha']
            Valor_fondeado = capital_data['Valor_fondeado']

            # Data for the pie chart of product type percentage
            porcentaje_madera_plastica = dic['porcentaje_madera_plastica']
            porcentaje_materia_prima = dic['porcentaje_materia_prima']
            porcentaje_productos_de_inyeccion = dic['porcentaje_productos_de_inyeccion']
            porcentaje_otros = dic['porcentaje_otros']

            # Create graphs with the given information
            Horizontal_Bar_Graph(
                Valor_fondeado, Valor_ejecutado_a_la_fecha,
                Valor_restante_para_ejecucion,
                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "images_for_report/img_valor_ejecutado_y_valor_restante.png")
            )

            pie_graph_towns(
                porcentaje_madera_plastica, porcentaje_materia_prima,
                porcentaje_productos_de_inyeccion, porcentaje_otros,
                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "images_for_report/img_type_of_products_towns.png")
            )

            # Fill the PDF with images, graphs, and text from MongoDB
            write_in_pdf_and_add_images(
                dic, os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                  "plantilla/Plantilla PM-SC1.pdf")
            )

            # Build a non-form PDF
            images_paths = [
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "final_images_for_report/page1.png"),
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "final_images_for_report/page2.png"),
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "final_images_for_report/page3.png"),
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "final_images_for_report/page4.png")
            ]
            images_to_pdf(images_paths)

        else:
            # Check if page 3 contains an image
            if dic['que_dice_la_empresa_con_imagen'].strip() == '':
                del dic['img_que_dice_la_empresa_posible_imagen']

            # Create images for the report
            cumplimiento_actual_del_proyecto = dic['porcentaje_cumplimiento_actual_del_proyecto']
            cumplimiento_actual_de_la_fase = dic['porcentaje_cumplimiento_actual_de_la_fase']
            capital_data = dic['Capital_del_Proyecto_en_ejecucion']
            Valor_restante_para_ejecucion = capital_data['Valor_restante_para_ejecucion']
            Valor_ejecutado_a_la_fecha = capital_data['Valor_ejecutado_a_la_fecha']
            Valor_fondeado = capital_data['Valor_fondeado']

            donut_graph(
                cumplimiento_actual_del_proyecto,
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                             "images_for_report/img_cumplimiento_actual_del_proyecto.png")
            )

            donut_graph(
                cumplimiento_actual_de_la_fase,
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                             "images_for_report/img_cumplimiento_actual_de_la_fase.png")
            )

            Horizontal_Bar_Graph(
                Valor_fondeado, Valor_ejecutado_a_la_fecha, Valor_restante_para_ejecucion,
                os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                             "images_for_report/img_valor_ejecutado_y_valor_restante.png")
            )

            # Fill the form PDF with the images
            write_in_pdf_and_add_images(
                dic, os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                  "plantilla/Plantilla Seguimientos.pdf")
            )

            # Create the final PDF for the report
            images_paths = []
            for i in range(1, 5):
                if dic['page4_va_o_no'] or i < 4:
                    images_paths.append(
                        os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                     "final_images_for_report/page{}.png".format(i))
                    )
            images_to_pdf(images_paths)

        # Send the email with the images and the PDF
        numero_de_mes = dic['numero_informe']
        numero_de_proyecto = dic['numero_del_proyecto']
        nombre_del_proyecto = dic['nombre_proyecto']
        emails = get_emails_by_project_id(dic['id_project'])
        if for_gv:
            contexto = 'Para los Greenvestors'
            emails = ['bry3639@gmail.com'] + emails
            mensaje = 'Procedimiento exitoso para los Greenvestors'
        else:
            contexto = 'de testeo'
            cantidad_gv = str(len(emails))
            emails = ['bry3639@gmail.com']
            mensaje = 'Procedimiento exitoso {} y se enviara a {} GreenVestors'.format(contexto, cantidad_gv)
        send_email(emails, numero_de_mes, numero_de_proyecto, nombre_del_proyecto, images_paths, dic['page4_va_o_no'])
        print('envio exitoso')

        # Update the PDF to Google Drive and Sheets for history tracking
        if for_gv:
            name = 'Informe_' + dic['numero_informe'] + '_' + dic['id_project']
            link_pdf = update_to_drive_pdf(name, dic['history_folder'])
            columna_objetivo = 'Mes ' + dic['numero_informe']
            write_in_sheets(dic['id_project'], columna_objetivo, link_pdf)
            print('Se subio el pdf al historial de forma exitosa')
        emails_gv = get_emails_by_project_id(dic['id_project'])

    return mensaje, emails_gv


# Testing
# print(reports_for_gv(['PM-SC1'],False))
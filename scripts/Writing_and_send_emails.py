import os
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image
from pymongo import MongoClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def emails_town_project(id_sheets):
    """
    Connect to a Google Sheet using service account credentials, 
    search for the 'CORREO' column, and return a list of emails after applying strip.

    :param id_sheets: The ID of the Google Sheet.
    :return: A list of email addresses.
    """
    # Configure credentials and client
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    creds_path = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               "credentials_service_account/clickgreen-099abcdc309c.json"))
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet using its ID
    sheet = client.open_by_key(id_sheets).worksheet('GREENVESTORS')

    # Find the 'CORREO' column
    email_col_index = sheet.find("CORREO").col
    emails = sheet.col_values(email_col_index)

    # Remove white spaces and filter out non-null values
    stripped_emails = [email.strip() for email in emails[1:] if email.strip()]

    return stripped_emails

def get_emails_by_project_id(id_project):
    """
    Check if the project is a town project or a regular project and retrieve emails accordingly.

    :param id_project: The project ID.
    :return: A list of email addresses.
    """
    # Check if the project is for towns or a regular project
    if id_project == 'PM-SC1':
        emails = emails_town_project('id_sheets')
    else:
        uri = os.environ.get('data_clickgreen')
        # Set up the MongoDB database connection
        client = MongoClient(uri)
        db = client["data"]  # Replace with your database name
        collection = db["old_users"]  # Replace with your collection name

        # Build the query
        query = {"projects_list." + id_project: {"$exists": True}}
        projection = {"email": 1}

        # Execute the query
        results = collection.find(query, projection)

        # Get email addresses
        emails = [doc["email"].split(' - ')[0].strip() for doc in results]

    return emails


def send_email(destinatarios, numero_de_mes, numero_de_proyecto, nombre_del_proyecto, imagenes_paths, page4_va_o_no):

    email = 'bry3639@gmaik.com'
    password = 'app_password'

    # Definimos una función auxiliar que envía correos a un grupo de destinatarios
    def enviar_grupo(destinatarios_grupo):
        # Crear el mensaje de correo
        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = "¡Ya está listo el reporte de tu proyecto con ClickGreen! 💚♻"
        mensaje["From"] = email
        mensaje["Bcc"] = ", ".join(destinatarios_grupo)  # Añadir los destinatarios del grupo como Bcc



        if page4_va_o_no ==True:
            # Añadir el cuerpo HTML del mensaje, que contiene las imágenes y un emoji
            corazon_verde_emoji = u'\U0001F49A'
            html = f"""\
            <html>
            <body>
                <p> ¡Hola Greenvestor! <br>
                    A continuación encontrarás los avances del mes {numero_de_mes} del proyecto {numero_de_proyecto} {nombre_del_proyecto}, si tienes alguna pregunta, no dudes en contactarnos a nuestro Whatsapp.💚 {corazon_verde_emoji}<br>
                </p>
                <div>
                    <img src="cid:imagen1" style="display:block;margin-bottom:10px;">
                    <img src="cid:imagen2" style="display:block;margin-bottom:10px;">
                    <img src="cid:imagen3" style="display:block;margin-bottom:10px;">
                    <img src="cid:imagen4" style="display:block;margin-bottom:10px;">
                </div>
            </body>
            </html>
            """
        else:
            # Añadir el cuerpo HTML del mensaje, que contiene las imágenes y un emoji
            corazon_verde_emoji = u'\U0001F49A'
            html = f"""\
            <html>
            <body>
                <p> ¡Hola Greenvestor! <br>
                    A continuación encontrarás los avances del mes {numero_de_mes} del proyecto {numero_de_proyecto} {nombre_del_proyecto}, si tienes alguna pregunta, no dudes en contactarnos a nuestro Whatsapp.💚 {corazon_verde_emoji}<br>
                </p>
                <div>
                    <img src="cid:imagen1" style="display:block;margin-bottom:10px;">
                    <img src="cid:imagen2" style="display:block;margin-bottom:10px;">
                    <img src="cid:imagen3" style="display:block;margin-bottom:10px;">
                    
                </div>
            </body>
            </html>
            """

        # Añadir el HTML al mensaje
        parte_html = MIMEText(html, "html")
        mensaje.attach(parte_html)

        # Cargar y redimensionar las imágenes
        
        for i, imagen_path in enumerate(imagenes_paths, start=1):
            imagen = Image.open(imagen_path)
            # Redimensionar la imagen a un tamaño adecuado para el correo
            nuevo_ancho = 800
            nuevo_alto = int(imagen.height * nuevo_ancho / imagen.width)
            imagen = imagen.resize((nuevo_ancho, nuevo_alto))

            # Guardar la imagen redimensionada en un archivo temporal
            imagen_temp_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"final_images_for_report/page{i}_resized.png")
            imagen.save(imagen_temp_path)

            # Añadir la imagen al mensaje
            with open(imagen_temp_path, "rb") as f:
                imagen_adjunta = MIMEImage(f.read())
            imagen_adjunta.add_header("Content-ID", f"<imagen{i}>")
            # Aquí añades el nombre que quieres darle a la imagen
            imagen_adjunta.add_header("Content-Disposition", f"inline; filename=imagen reporte {i}.png")
            mensaje.attach(imagen_adjunta)

        # Adjuntar PDF

        ruta_pdf = os.path.join(os.path.dirname(os.path.realpath(__file__)), "final_images_for_report/Informe_Mensual.pdf")  # Reemplazar con la ruta del archivo PDF
        nombre_pdf = "Informe_Mensual.pdf"  # Esto es lo que los destinatarios verán
        with open(ruta_pdf, "rb") as archivo:
            adjunto = MIMEBase("application", "octet-stream")
            adjunto.set_payload(archivo.read())
        encoders.encode_base64(adjunto)
        adjunto.add_header(
            "Content-Disposition",
            f"attachment; filename= {nombre_pdf}",
        )
        mensaje.attach(adjunto)

        # Enviar el correo
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, password)
            server.send_message(mensaje)
    # Dividimos la lista de destinatarios en grupos de 98
    num_grupos = math.ceil(len(destinatarios) / 98)
    for i in range(num_grupos):
        inicio = i * 98
        fin = inicio + 98
        destinatarios_grupo = destinatarios[inicio:fin]
        enviar_grupo(destinatarios_grupo)

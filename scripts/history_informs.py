import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import os

def write_in_sheets(row_target, column_target, link):
    """
    Write a link in a specific cell in a Google Sheets.

    Args:
    - row_target: The target row for the link.
    - column_target: The target column for the link.
    - link: The link to be written in the cell.
    """
    # Use the downloaded JSON file to authorize your service account
    credentials_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                    "credentials_service_account/clickgreen-099abcdc309c.json")
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scopes)

    # Log in to the Google Sheets API with your credentials
    client = gspread.authorize(credentials)

    # Open the Google Sheet using its ID (make sure to share the Google Sheet with your service account)
    workbook = client.open_by_key('Id_sheets')

    # Select a sheet within the workbook by its name
    sheet = workbook.worksheet('Informes')

    # Get the values of the first row and column
    first_row = sheet.row_values(1)
    first_column = sheet.col_values(1)

    # Find the corresponding indices (add 1 as rows/columns in Google Sheets start from 1, not 0)
    row_index = first_column.index(row_target) + 1
    column_index = first_row.index(column_target) + 1

    # Update the corresponding cell
    sheet.update_cell(row_index, column_index, link)


def update_to_drive_pdf(name, link_folder):
    """
    Upload a PDF file to Google Drive and return its web view link.

    Args:
    - name: The name of the PDF file to be uploaded.
    - link_folder: The Google Drive folder link where the file will be uploaded.

    Returns:
    - The web view link of the uploaded PDF file.
    """
    # Extract the folder ID from the link
    id_folder = link_folder.split('/')[-1]

    # Load the service account credentials
    credentials_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                    "credentials_service_account/clickgreen-099abcdc309c.json")
    creds = Credentials.from_service_account_file(credentials_path)

    # Create the Drive service
    service = build('drive', 'v3', credentials=creds)

    # Path to the monthly report
    monthly_report_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                       "final_images_for_report/Informe_Mensual.pdf")

    # Create the media object for upload
    media = MediaFileUpload(monthly_report_path, 
                            mimetype='application/pdf', 
                            resumable=True)

    # Create the Drive file metadata
    file_metadata = {
        'name': name,
        'parents': [id_folder]
    }

    # Upload the file to Drive
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id, webViewLink').execute()

    return file.get('webViewLink')

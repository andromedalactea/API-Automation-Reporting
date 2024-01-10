# Standard library imports
import io
import os

# Third party imports
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties

#----------------------------------------------------------------------------------
# Donut Graph

def donut_graph(percent, path_to_save, path_font=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Fonts/RedHatDisplay-VariableFont_wght.ttf")): 
    """
    Function to create a donut graph to represent a percentage.

    Args:
    - percent (float): The percentage to be represented.
    - path_to_save (str): Path where the graph will be saved.
    - path_font (str, optional): Path to the custom font file. Defaults to a path in the 'Fonts' directory.
    """
    prop = font_manager.FontProperties(fname=path_font)
    # Percentage to represent
    porcentaje = percent
    # Create the data
    data = [porcentaje, 100 - porcentaje]
    # Normalize RGB values
    colors = [(228/255, 85/255, 12/255), (26/255, 137/255, 0)]  # orange, green

    # Create the donut chart
    fig, ax = plt.subplots()
    fig.set_size_inches(2.2, 2.2)  # Set the size of the chart in inches

    # Create the donut chart with a gap between the segments
    wedges, texts = ax.pie(data, labels=None, colors=colors, startangle=90, 
                        wedgeprops=dict(width=0.3, edgecolor='w', linewidth=2))

    # Create the label in the center
    plt.text(0, 0, f'{porcentaje}%', ha='center', va='center', fontsize=20, fontweight='bold')

    # Equalize the x and y axis dimensions so the chart is circular
    plt.axis('equal')

    # Save the chart as a PNG image
    plt.savefig(path_to_save, transparent=False, bbox_inches='tight', pad_inches=0)


#------------------------------------------------------------------------------------------------------------------
# Horizontal Bar Graph

def Horizontal_Bar_Graph(Valor_fondeado, Valor_ejecutado_a_la_fecha, Valor_restante_para_ejecucion, path_to_save, path_font=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Fonts/RedHatDisplay-VariableFont_wght.ttf")):
    """
    Function to create a horizontal bar graph to visualize three financial values:
    funded value, value executed to date, and remaining value for execution.

    Args:
    - Valor_fondeado (float): Funded value.
    - Valor_ejecutado_a_la_fecha (float): Value executed to date.
    - Valor_restante_para_ejecucion (float): Remaining value for execution.
    - path_to_save (str): Path where the graph will be saved.
    - path_font (str, optional): Path to the custom font file. Defaults to a path in the 'Fonts' directory.
    """

    prop = font_manager.FontProperties(fname=path_font)

    # Create some data
    categories = ['Remaining value for execution', 'Value executed to date', 'Funded value']
    values = [Valor_restante_para_ejecucion, Valor_ejecutado_a_la_fecha, Valor_fondeado]

    # Create a figure with custom dimensions (width, height)
    fig, ax = plt.subplots(figsize=(1350/100, 400/100))

    # Create a horizontal bar graph
    ax.barh(categories, values, color=(26/255, 137/255, 0), edgecolor='none')

    # Remove the outline
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add grid lines on the X-axis
    ax.xaxis.grid(True, color='gray', linestyle='dashed', linewidth=0.6, alpha=0.7)
    ax.yaxis.grid(False)  # Hide grid lines on the Y-axis

    # Increase the font size for the axes
    ax.tick_params(axis='both', labelsize=24) 

    # Hide tick marks on the axes
    ax.tick_params(axis='both', which='both', length=0)

    # Format function for the X-axis
    def format_func(value, tick_number):
        return '$%dM' % (value)

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_func))

    # Set the number of ticks on the X-axis
    ax.xaxis.set_major_locator(mticker.MaxNLocator(5))

    # Adjust the Y-axis limits to leave space for the legend
    ax.set_ylim(-0.5, len(categories)-0.5)

    # Add a title to the graph
    ax.set_title('Project Capital in Execution', fontsize=24)

    # Save the figure
    plt.savefig(path_to_save, transparent=False, bbox_inches='tight', pad_inches=0)


#-----------------------------------------------------------------------------------------------------------
# Pie Chart
def pie_graph_towns(madera_plastica_percent, materia_prima_percent, productos_inyeccion_percent, otros_percent, path_to_save):
    """
    Function to create a pie chart with the distribution percentages of four categories:
    plastic wood, raw material, injection products, and others.

    Args:
    - madera_plastica_percent (float): Percentage of plastic wood.
    - materia_prima_percent (float): Percentage of raw material.
    - productos_inyeccion_percent (float): Percentage of injection products.
    - otros_percent (float): Percentage of others.
    - path_to_save (str): Path where the graph will be saved.

    If all values are zero, each category is set to 25% and a custom '0%' label is set for all categories.
    """

    # Check if all values are zero
    if madera_plastica_percent == materia_prima_percent == productos_inyeccion_percent == otros_percent == 0:
        sizes = [25, 25, 25, 25]  # Set each category to 25%
        autopct_labels = ['0%']  # Only a '0%' label
    else:
        sizes = [madera_plastica_percent, materia_prima_percent, productos_inyeccion_percent, otros_percent]
        autopct_labels = '%1.0f%%'  # Percentage format for non-zero values

    labels = ['Plastic Wood', 'Injection Products', 'Raw Material', 'Others']
    colors = ['#78C505', '#C1FF72', '#7ED957', '#00BF63']

    # Create a figure and a set of subplots
    fig, ax = plt.subplots()

    # Pie chart
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct=lambda pct: autopct_labels[0] if isinstance(autopct_labels, list) else autopct_labels % pct,
        startangle=90,
        pctdistance=0.75
    )

    # Text settings
    plt.setp(autotexts, size=15, color="black")
    plt.setp(texts, size=15, color="black")

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')  

    # Position and title adjustments
    ax.set_position([0.1, 0.1, 0.75, 0.75])
    plt.title(' ', pad=20)
    plt.tight_layout()

    # Save the chart
    plt.savefig(path_to_save, transparent=False, bbox_inches='tight', pad_inches=0)

#-------------------------------------------------------------------------------------------------------
# Download images of google drive folde specified in Mongo information
def download_images_of_project(link_folder):
    """
    Function to download images from a Google Drive folder.

    Args:
    - link_folder (str): The link to the Google Drive folder.

    The function loads the service account credentials, creates the Drive service,
    extracts the folder ID from the link, lists the files in the folder, and downloads
    specified files to a local directory.
    """

    # Load service account credentials
    path_credentials = os.path.join(os.path.dirname(os.path.realpath(__file__)), "credentials_service_account")
    creds = Credentials.from_service_account_file(path_credentials)

    # Create the Drive service
    service = build('drive', 'v3', credentials=creds)

    # Folder ID
    folder_id = link_folder.split('/')[-1]

    # Names of the files you want to download (without the extension)
    file_names = ['1', '2']

    # List the files in the folder
    results = service.files().list(q=f"'{folder_id}' in parents").execute()
    items = results.get('files', [])
    
    download_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images_for_report")  # Full path to the local folder

    for item in items:
        if os.path.splitext(item['name'])[0] in file_names:  # Compare the name without the extension
            file_id = item['id']
            request = service.files().get_media(fileId=file_id)
            file_path = os.path.join(download_folder, f'{item["name"]}')  # Full path to the local file (includes the original extension)
            fh = io.FileIO(file_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            
# Testing usage 
# Horizontal_Bar_Graph(350,350,0,os.path.join(os.path.dirname(os.path.realpath(__file__)), "images_for_report/img_valor_ejecutado_y_valor_restante.png"))
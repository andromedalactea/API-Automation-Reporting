import os
from fpdf import FPDF
from pdf2image import convert_from_path
import pdfrw
from PIL import Image

def write_in_pdf_and_add_images(dictionary, input_pdf_path):
    """
    Fill a PDF template with text and images from a dictionary, and save as images.

    Args:
    - dictionary: Dictionary containing text and image information.
    - input_pdf_path: Path to the input PDF template.
    """
    output_pdf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                   "final_images_for_report/pdf_fill_text.pdf")
    template = pdfrw.PdfReader(input_pdf_path)

    # Iterate through the pages and form fields
    for page in template.pages:
        annotations = page['/Annots']
        if annotations is not None:
            filled_fields = []  # List to store names of filled fields on each page

            for annotation in annotations:
                if annotation['/Subtype'] == '/Widget' and '/T' in annotation:
                    field_name = annotation['/T'][1:-1]
                    if field_name in dictionary:
                        annotation.update(pdfrw.PdfDict(V='{}'.format(dictionary[field_name])))
                        filled_fields.append(field_name)

            # Hide overlapping fields on the page
            for annotation in annotations:
                if annotation['/Subtype'] == '/Widget' and '/T' in annotation:
                    field_name = annotation['/T'][1:-1]
                    if field_name not in filled_fields:
                        annotation.update(pdfrw.PdfDict(F=1))  # Hide the field using /F property

    # Save the filled PDF to a new file
    pdfrw.PdfWriter().write(output_pdf_path, template)

    # Convert the PDF to images
    pages = convert_from_path(output_pdf_path)

    # Iterate through the pages
    for i, page in enumerate(pages):
        for key, value in dictionary.items():
            if key.startswith('img_') and value['page'] == i+1:
                img = Image.open(value['path'])
                img = img.resize((value['width'], value['height']))
                page.paste(img, (value['x'], value['y']))

        path_to_save = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                    "final_images_for_report")
        page.save(path_to_save + '/page' + str(i+1) + '.png', 'PNG')

def images_to_pdf(images_paths, output_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                                         "final_images_for_report/Informe_Mensual.pdf")):
    """
    Convert a list of image paths to a single PDF file.

    Args:
    - images_paths: List of paths to the images.
    - output_path: Path for the output PDF file.
    """
    first_image = Image.open(images_paths[0])
    width, height = first_image.size

    # Convert dimensions to points (1 inch = 72 points)
    width, height = width * 0.75, height * 0.75

    # Create an FPDF instance with the size of the first image
    pdf = FPDF(unit="pt", format=(width, height))

    # Iterate over each image
    for image_path in images_paths:
        pdf.add_page()
        pdf.image(image_path, 0, 0, width, height)

    # Save the PDF to the output path
    pdf.output(output_path, "F")



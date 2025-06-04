from PIL import Image
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for page in images:
        text += pytesseract.image_to_string(page) + "\n"
    return text

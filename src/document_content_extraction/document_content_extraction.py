from PIL import Image
import pytesseract

class DocumentContentExtraction:
    def __init__(self):
        pass


if __name__=="__main__":



    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    # OCR processing
    image = Image.open('/Users/imansaberi/Documents/research_projects/content_extraction/VGT/high-res-output/page_0.png')
    text = pytesseract.image_to_string(image)
    print(text)
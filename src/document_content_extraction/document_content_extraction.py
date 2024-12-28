from PIL import Image
import pytesseract
from src.document_content_extraction.scene import Scene

class DocumentContentExtraction:
    def __init__(self):
        pass

    def process(self,input_image,scenes:list[Scene]):
        # Crop the image to the bounding box
        image = Image.open(input_image)
        for scene in scenes:
            contents = []
            for comp in scene.components:
                cropped_image = image.crop(comp)
                contents.append(pytesseract.image_to_string(cropped_image))
            scene.content = contents
        return scenes
        


if __name__=="__main__":



    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    # OCR processing
    image = Image.open('/Users/imansaberi/Documents/research_projects/content_extraction/VGT/high-res-output/page_0.png')
    text = pytesseract.image_to_string(image)
    print(text)
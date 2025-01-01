from PIL import Image
import pytesseract
from src.document_content_extraction.scene import Scene
from openai import OpenAI 

class DocumentContentExtraction:
    def __init__(self):
        self.client = OpenAI(api_key="sk-3a1e3c8c84c64d8aa0af38575f06529a", base_url="https://api.deepseek.com")

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
    
    def convert_to_narrative_form(self,scenes:list[Scene]):
        content = [ f"Section {i}:\n" + str(scene.content) for i,scene in enumerate(scenes) ]
    
        response = self.client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an academic paper reviewer. I will send you the paper section by section. For each section, provide a narrative explanation that summarizes and contextualizes its content. You SHOULD only explain the provided contents and in a narrative format. Each section should start with Section n:, where n is the number of section. Each section should be separated by '---'. Ensure that your explanation maintains a clear and narrative form, generate the explanations per each section:"},
            {"role": "user", "content": str(content)},
        ],
        stream=False
    )
        
        print(response.choices[0].message.content)
        


if __name__=="__main__":



    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    # OCR processing
    image = Image.open('/Users/imansaberi/Documents/research_projects/content_extraction/VGT/high-res-output/page_0.png')
    text = pytesseract.image_to_string(image)
    print(text)
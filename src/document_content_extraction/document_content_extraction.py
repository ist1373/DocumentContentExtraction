from PIL import Image
import pytesseract
from src.document_content_extraction.scene import Scene
from openai import OpenAI 
import re

class DocumentContentExtraction:
    def __init__(self):
        self.client = OpenAI(api_key="sk-3a1e3c8c84c64d8aa0af38575f06529a", base_url="https://api.deepseek.com")

    def check_if_empty(self,arr):
        string = "".join(arr).strip()
        return string == ""

    def summarize_previous_content(self,content):  
            system_prompt = """
                You are an academic paper summarizer. Summarize the following content in one paragraphs:
            """
            messages = [
                {"role": "system", "content": system_prompt} ,
                {"role": "user", "content": str(content)}
                ]
            response = self.client.chat.completions.create(
            model="deepseek-chat", messages=messages, stream=False)
            return response.choices[0].message.content 
    
    
    def process(self,input_image,scenes:list[Scene]):
        # Crop the image to the bounding box
        image = Image.open(input_image)
        new_scenes = []
        for i,scene in enumerate(scenes):
            contents = []
            for comp in scene.components:
                cropped_image = image.crop(comp)
                contents.append(pytesseract.image_to_string(cropped_image))

            if self.check_if_empty(contents):
                pass
            else:
                scene.content = contents 
                new_scenes.append(scene)
        return new_scenes
    
    def convert_to_narrative_form_v1(self,scenes:list[Scene]):
        content = [ f"Section {i}:\n" + str(scene.content) for i,scene in enumerate(scenes) ]
    
        response = self.client.chat.completions.create(
        model="deepseek-chat",
        # messages=[
        #     {"role": "system", "content": "You are an academic paper reviewer. I will send you the paper section by section. For each section, provide a narrative explanation that summarizes its content. You SHOULD only explain the provided contents and in a narrative format. Each section should start with Section n:, where n is the number of section. Each section should be separated by '---'. Ensure that your explanation maintains a clear and narrative form, generate the explanations per each section:"},
        #     {"role": "user", "content": str(content)},
        # ],stream=False)
        messages=[
            {"role": "system", "content": "You are an excited youtuber that want to review an academic paper. I will send you a paper section by section. For each section, provide a breif summary only containes the key points of each section. Each section should start with Section n:, where n is the number of section. Each section should be separated by '---'. Ensure that your explanation is consice and to the point."},
            {"role": "user", "content": str(content)},
        ],stream=False)
        
        response = response.choices[0].message.content
        print(response)
        sections = self.remove_meta_data(response)
        for i,scene in enumerate(scenes):
            scene.narrative_content = sections[i]
        return scenes
    

    def convert_to_narrative_form_v2(self,scenes:list[Scene],prev_conversations = []):
        content = [ f"Section {i}:\n" + str(scene.content) for i,scene in enumerate(scenes) ]
    
        system_prompt = """
            You are an enthusiastic YouTuber reviewing an academic paper. I will provide the paper section by section. For each section:

            * Start with "**Section n:**", where n represents the section number.
            * Provide a concise summary highlighting only the key points.
            * Ensure that the summaries are clear, focused, and to the point.
            * Separate summaries for each section with "---".
        """
        # messages = [
        #     {"role": "system", "content": "You are an excited youtuber that want to review an academic paper. I will send you a paper section by section. For each section, provide a breif summary only containes the key points of each section. Each section should start with Section n:, where n is the number of section. Each section should be separated by '---'. Ensure that your explanation is consice and to the point."}, 
        # ]

        messages = [
            {"role": "system", "content": system_prompt} 
            ]

        messages = messages +  prev_conversations
        new_message = {"role": "user", "content": str(content)}
        messages.append(new_message)

        response = self.client.chat.completions.create(
        model="deepseek-chat", messages=messages, stream=False)
        
        response = response.choices[0].message.content
        new_response = {"role": "assistant", "content": str(response)}

        prev_conversations.append(new_message)
        prev_conversations.append(new_response)

        sections = self.remove_meta_data(response)

        for i,scene in enumerate(scenes):
            scene.narrative_content = sections[i]
        return scenes,prev_conversations


    def convert_to_narrative_form_v3(self,scenes:list[Scene],prev_summary = ""):
        content = [ f"Section {i}:\n" + str(scene.content) for i,scene in enumerate(scenes) ]

        if prev_summary == "":

            system_prompt = """
                You are an enthusiastic YouTuber reviewing an academic paper. I will provide the paper section by section. For each section:

                * Start with "**Section n:**", where n represents the section number.
                * Provide a concise and precise summary highlighting the key points.
                * Ensure that the summaries are clear, focused, and to the point.
                * Summarize the content in the same order it is presented in the section.
                * Separate summaries for each section with "---".
            """
        else:
            system_prompt = f"""
                You are an enthusiastic YouTuber reviewing an academic paper. You are in the middle of reviewing. I will provide the rest of the paper section by section. For each section:

                * Start with "**Section n:**", where n represents the section number.
                * Provide a concise and precise summary highlighting the key points.
                * Ensure that the summaries are clear and to the point.
                * Summarize the content in the same order it is presented in the section.
                * Separate summaries for each section with "---".

                To help you avoid repetition, here’s the content you've already summarized:
                {prev_summary}
                End of previous summary.
            """            
        messages = [
            {"role": "system", "content": system_prompt} ,
            {"role": "user", "content": str(content)}
            ]


        response = self.client.chat.completions.create(
        model="deepseek-chat", messages=messages, stream=False)
        
        response = response.choices[0].message.content

        sections = self.remove_meta_data(response)

        explained_content = prev_summary + "\n" + "\n".join(sections)

        summarized_prev_content = self.summarize_previous_content(explained_content)
        for i,scene in enumerate(scenes):
            scene.narrative_content = sections[i]
        return scenes, summarized_prev_content
        
    def get_response(self, content):
        # Add user input to the conversation
        self.messages.append({"role": "user", "content": str(content)})

        # Get response from the model
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            stream=False,
        )

        # Extract assistant's reply and add it to the conversation history
        assistant_message = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message
        
    def remove_meta_data(self,response:str):
        sections = response.split("---")
        cleaned_sections = [re.sub(r"\*\*Section \d+:\*\*\s*", '', section, flags=re.MULTILINE) for section in sections]
        return cleaned_sections

if __name__=="__main__":



    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    # OCR processing
    image = Image.open('/Users/imansaberi/Documents/research_projects/content_extraction/VGT/high-res-output/page_0.png')
    text = pytesseract.image_to_string(image)
    print(text)
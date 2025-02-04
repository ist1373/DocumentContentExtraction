from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from subprocess import run, CalledProcessError
import os
from src.document_content_extraction.document_content_extraction import DocumentContentExtraction
from src.document_content_extraction.scene import Scene
from fastapi.responses import ORJSONResponse
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


app = FastAPI()
document_content_extractor = DocumentContentExtraction()

class SceneModel(BaseModel):
    components: list[list[float]]
    x1: float
    y1: float
    x2: float
    y2: float
    zoom_factor:float

class ScenesModel(BaseModel):
    scenes:list[SceneModel]
    prev_summary:str
    input_image:str


@app.post("/extract-contents/")
def extract_contents(input_args: ScenesModel):
    try:
        scenes = []
        for scene in input_args.scenes:
            scenes.append(Scene(scene.x1,scene.y1,scene.x2,scene.y2,scene.components,scene.zoom_factor))

        scenes = document_content_extractor.process(input_args.input_image,scenes)
        scenes,summary = document_content_extractor.convert_to_narrative_form_v3(scenes,prev_summary=input_args.prev_summary)
        return {"status": "success", "scenes": scenes,"prev_summary":summary}
    except CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
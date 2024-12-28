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
    input_image:str


@app.post("/extract-contents/")
def plan_scences(scene_args: ScenesModel):
    try:
        scenes = []
        for scene in scene_args.scenes:
            scenes.append(Scene(scene.x1,scene.y1,scene.x2,scene.y2,scene.components,scene.zoom_factor))

        scenes = document_content_extractor.process(scene_args.input_image,scenes)

        return {"status": "success", "output": scenes}
    except CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
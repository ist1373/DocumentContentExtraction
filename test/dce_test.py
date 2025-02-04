import unittest
from src.document_content_extraction.document_content_extraction import DocumentContentExtraction
from src.document_content_extraction.scene import Scene
from app import SceneModel,ScenesModel


input_data = ScenesModel(
        input_image="./test/data/page_0.png",
        prev_summary="",
        scenes=[
            SceneModel(
                components=[
                    [108.0, 101.0, 1116.0, 209.0],
                    [178.0, 242.0, 1038.0, 340.0],
                    [231.0, 366.0, 993.0, 464.0]
                ],
                x1=0,
                y1=76.0,
                x2=1224,
                y2=611.0,
                zoom_factor=1
            ),
            SceneModel(
                components=[
                    [96.0, 531.0, 601.0, 850.0],
                    [96.0, 851.0, 601.0, 956.0]
                ],
                x1=0,
                y1=506.0,
                x2=1224,
                y2=1041.0,
                zoom_factor=1
            ),
            SceneModel(
                components=[
                    [96.0, 966.0, 600.0, 1395.0],
                    [113.0, 1418.0, 364.0, 1436.0]
                ],
                x1=0,
                y1=941.0,
                x2=1224,
                y2=1476.0,
                zoom_factor=1
            ),
            SceneModel(
                components=[
                    [622.0, 530.0, 1127.0, 911.0]
                ],
                x1=0,
                y1=505.0,
                x2=1224,
                y2=1040.0,
                zoom_factor=1
            ),
            SceneModel(
                components=[
                    [622.0, 913.0, 1127.0, 1437.0]
                ],
                x1=0,
                y1=888.0,
                x2=1224,
                y2=1423.0,
                zoom_factor=1
            ),
        ]
    )

class TestConvertPdfToImage(unittest.TestCase):
    
    def test_convert_pdf_to_image(self):
        document_content_extractor = DocumentContentExtraction()

        scenes = []
        for scene in input_data.scenes:
            scenes.append(Scene(scene.x1,scene.y1,scene.x2,scene.y2,scene.components,scene.zoom_factor))
        scenes = document_content_extractor.process(input_data.input_image,scenes)
        scenes,summary = document_content_extractor.convert_to_narrative_form_v3(scenes,prev_summary=input_data.prev_summary)
        self.assertEqual(scenes[0].content[0],"AdvFusion: Adapter-based Knowledge Transfer for\nCode Summarization on Code Language Models\n")


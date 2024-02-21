import tempfile
import os
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, File, UploadFile
from dotenv import load_dotenv
from .utils.prompts import TRAINING_PROMPT_LEGIT, TRAINING_PROMPT_CHEAT, BASE_PROMPT
from .utils.process import ESPAnalyzer
load_dotenv()

router = APIRouter()

esp_analyzer = ESPAnalyzer(openai_api_key=os.getenv("OPENAI_API_KEY"))



@router.post("/analyze")
async def analyze(file: UploadFile):
    """
    This endpoint is used to input data to be analyzed for unfair advantages in-game.
    """

    file_extension_allowed_list = ["jpeg", "jpg", "png"]
    if file.filename.split(".")[-1] not in file_extension_allowed_list:
        raise HTTPException(status_code=400, detail="File type not supported. Please use a jpeg, jpg, or png file.")
    
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, file.filename)
    
    with open(temp_file_path, 'wb+') as temp_file:
        temp_file.write(await file.read())
        inputted_encoded_image = esp_analyzer.encode_image(temp_file_path)
        cheating_example_image_base_64 = esp_analyzer.encode_image(image_path='training_data/examples/cheat/esp.jpeg')
        legit_example_image_base_64 = esp_analyzer.encode_image(image_path='training_data/examples/legit/legit.jpg')

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": TRAINING_PROMPT_CHEAT},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{cheating_example_image_base_64}"}}
                ]
            },
            {"role": "user", "content": [
                {"type": "text", "text": TRAINING_PROMPT_LEGIT},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{legit_example_image_base_64}"}}
                ]
            },
            {"role": "user", "content": [
                {"type": "text","text": BASE_PROMPT},
                {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{inputted_encoded_image}"}}
                ]
            }
            ],
            "max_tokens": 300
        }
        vision_model_response = esp_analyzer.process(payload)
        result = esp_analyzer.parse_response(vision_model_response)
        return result
    
   
import base64
from openai import OpenAI # openai version 1.1.1
import instructor
import requests
from pydantic.main import BaseModel
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logfile.txt')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class OutputModel(BaseModel):
    esp: bool
    
class ESPAnalyzer():
    def __init__(self, openai_api_key: str) -> None:
        self.openai_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }
        self.instructor_client = instructor.patch(
            client=OpenAI(api_key=openai_api_key)
        )

    def encode_image(self, image_path) -> str:
        logger.debug(f"Encoding image: {image_path}")
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def process(self, payload: dict) -> str:
        logger.debug(f"Sending payload to OpenAI (Non-Parsed)")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.openai_headers, json=payload)
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        logger.debug(f"Response from OpenAI (Non-Parsed): {content}")
        return content
    
    def parse_response(self, content: str) -> bool:
        parsed = self.instructor_client.chat.completions.create(
            model="gpt-4",
            response_model=OutputModel,
            messages=[
                {"role": "user", "content": "Is the person shown playing the game in the screenshot using ESP?" + content},
            ]
        )
        return parsed
        
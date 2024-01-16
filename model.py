import google.generativeai as genai
from IPython.display import Markdown
import PIL.Image
import pyautogui
genai.configure(api_key="AIzaSyAqNmllczUTlKBq7GbXCDe5NpiIR2hVETU")

generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 50,
}
# safety_settings = [
#   {
#     "category": "HARM_CATEGORY_HARASSMENT",
#     "threshold": "BLOCK_NONE"
#   },
#   {
#     "category": "HARM_CATEGORY_HATE_SPEECH",
#     "threshold": "BLOCK_NONE"
#   },
#   {
#     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#     "threshold": "BLOCK_NONE"
#   },
#   {
#     "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#     "threshold": "BLOCK_NONE"
#   },
# ]

safety_settings = {
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}

model = genai.GenerativeModel(
    model_name="gemini-pro",
    # generation_config=generation_config,
    safety_settings=safety_settings
)




model_vision = genai.GenerativeModel('gemini-pro-vision',
                                    #  generation_config=generation_config,
                                     safety_settings=safety_settings)

chat = model.start_chat()

chat_vision = model_vision.start_chat()


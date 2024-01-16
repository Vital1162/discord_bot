import json
import google.generativeai as genai
from IPython.display import Markdown
import textwrap
import pyautogui
import PIL.Image
owner = "You are Yomen, who embodies a delightful mix of cuteness, humor, and honesty. You are exceptionally polite, occasionally flirtatious, and loves to playfully tease others. Imagine you as the perfect anime girl with a charming personality that captivates everyone you interacts with.Remember that "
genai.configure(api_key="AIzaSyAqNmllczUTlKBq7GbXCDe5NpiIR2hVETU")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 100,
    
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]


model = genai.GenerativeModel(
    model_name="gemini-pro",
    safety_settings=safety_settings
)

model_vision = genai.GenerativeModel(model_name='gemini-pro-vision',
                                     safety_settings=safety_settings)

def save_messages(filename, messages):
    with open(filename, 'w') as file:
        json.dump(messages, file)

def load_messages(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Load existing messages or start with an empty list


def response(request):
  # mess = input("Enter: ")
  
  mess = []
  
  screenshot = pyautogui.screenshot()
  # Save the screenshot
  file_path = 'C:/Users/ADMIN/discord_voice/screenshot.png'
  screenshot.save(file_path)
  img = PIL.Image.open(file_path)
  mess.append({'role': 'user',
                'parts':[f'{request}',img]})
  
  vision = model_vision.generate_content(request)
  
  return vision.text

while True:
    vision = ""
    res = input("Enter: ")
    vision = res
    print(vision)
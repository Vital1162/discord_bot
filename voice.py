import pyttsx3
engine = pyttsx3.init('sapi5')

rate = engine.getProperty('rate')
engine.setProperty('rate', 150)


volume = engine.getProperty('volume')

engine.setProperty('volume',1.0)

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[2].id)
# # engine.say('<pitch middle="10">That how much I love you</pitch>')

# engine.runAndWait()

def make_response(response):
    engine.save_to_file(f'<pitch middle="10">{response}</pitch>', 'response.mp3')
    engine.runAndWait()

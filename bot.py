import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import json
import os
import pyautogui
import PIL.Image
from model import model,chat, chat_vision,model_vision
from voice import make_response
import asyncio
import speech_recognition as sr

import time
import speech_recognition as sr
import pyttsx3
import functools
import typing
import asyncio
from discord import FFmpegPCMAudio
from io import BytesIO


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))

owner = ""
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# vision_text = "doing nothing"

def save_messages(filename, messages):
    with open(filename, 'w') as file:
        json.dump(messages, file)

def load_messages(filename):
    with open(filename, 'r') as file:
        return json.load(file)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # vision.start()



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    request = message.content
    if message.author.id == OWNER_ID:
        try:
            mess = load_messages('messages.json')
        except FileNotFoundError:
            mess = []
            mess.append({'role': 'user',
                        'parts':[owner]})
            reply = model.generate_content(mess)
            reply.resolve()
            mess.append({'role': 'model',
                        'parts': [reply.text]})
        

        screenshot = pyautogui.screenshot()
        # Save the screenshot
        
        file_path = 'C:/Users/ADMIN/discord_voice/screenshot.png'
        screenshot.save(file_path)
        img = PIL.Image.open(file_path)
        vision = model_vision.generate_content(["What is user doing right now ?, take a short describe no details about what is user doing right now? You reply with brief or funny, to-the-point answers with no elaboration",img],stream=True)
        vision.resolve()
        # print(vision.text)

        mess.append({'role': 'user',
                    'parts':[f'{request} and {vision.text}']})
    # else:
    #     mess.append({'role': 'user',
    #              'parts':[request]})
    else:
        print("not onwer")
        try:
            mess = load_messages(f'{message.author.id}.json')
        except FileNotFoundError:
            mess = []
            mess.append({'role': 'user',
                        'parts':[owner]})
            reply = model.generate_content(mess)
            reply.resolve()
            mess.append({'role': 'model',
                        'parts': [reply.text]})
        


        mess.append({'role': 'user',
                    'parts':[f'{request}']})

    # print(mess)
    response = model.generate_content(mess)
    response.resolve()



    mess.append({'role': 'model',
                'parts':[response.text]})

    if message.author.id == OWNER_ID:
        save_messages('messages.json', mess)
    else:
        save_messages(f'{message.author.id}.json',mess)

    await message.channel.send(response.text)



async def speak_to_user(voice_channel):
    try:
        mess = load_messages('messages.json')
    except FileNotFoundError:
        mess = []

        mess.append({'role': 'user',
                    'parts':[owner]})
        reply = model.generate_content(mess)
        reply.resolve()
        mess.append({'role': 'model',
                    'parts': [reply.text]})
    
    screenshot = pyautogui.screenshot()
    # Save the screenshot
    file_path = 'C:/Users/ADMIN/discord_voice/screenshot.png'
    screenshot.save(file_path)
    img = PIL.Image.open(file_path)
    vision = model_vision.generate_content(["What is your friend doing right now, make a really short describe no details about what is user doing right now? You reply with brief or funny, to-the-point answers with no elaboration",img],stream=True)
    vision.resolve()
    print(vision.text)

    mess.append({'role': 'user',
                'parts':[f'{vision.text}']})
    
    response = model.generate_content(mess,stream=True)
    response.resolve()
    print(response.text)
        
    # mess.append({'role': 'model',
    #             'parts':[response.text]})
    # save_messages('messages.json', mess)
    make_response(response.text)
    
    voice_channel.play(discord.FFmpegPCMAudio('response.mp3'))
    while voice_channel.is_playing():
        await asyncio.sleep(1)



@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == OWNER_ID:
        if before.channel != after.channel and not after.mute:
            if after.channel is not None:
                # Member joined a voice channel
                voice_channel = await after.channel.connect()
                await listen_and_respond(voice_channel)
            elif before.channel is not None:
                # Member left a voice channel
                for vc in bot.voice_clients:
                    if vc.channel.guild == member.guild:
                        await vc.disconnect()

recognizer = sr.Recognizer()
async def listen_and_respond(voice_channel):
    timeout = 0
    while True:
        if not voice_channel.is_connected() or not voice_channel.guild.get_member(OWNER_ID).voice:
            break
        # Check if the user is muted
        if voice_channel.guild.get_member(OWNER_ID).voice.self_mute:
            await asyncio.sleep(1)
            
            continue
        with sr.Microphone() as source:
            print("Say something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

            try:
                mess = load_messages('messages.json')
            except FileNotFoundError:
                mess = []

                mess.append({'role': 'user',
                            'parts':[owner]})
                reply = model.generate_content(mess)
                reply.resolve()
                mess.append({'role': 'model',
                            'parts': [reply.text]})
            
            screenshot = pyautogui.screenshot()
            # Save the screenshot
            file_path = 'C:/Users/ADMIN/discord_voice/screenshot.png'
            screenshot.save(file_path)
            img = PIL.Image.open(file_path)
      
            vision = model_vision.generate_content(["What is your friend doing right now, make a really short describe no details about what is user doing right now? You reply with brief or funny, to-the-point answers with no elaboration",img],stream=True)

            vision.resolve()
            print(vision.text)

            mess.append({'role': 'user',
                        'parts':[f'{text} \n {vision.text}']})

            response = model.generate_content(mess,stream=True)

            response.resolve()
            print(f"Bot's response: {response.text}")

            # Convert the text response to speech
            make_response(response.text)

            voice_channel.play(discord.FFmpegPCMAudio('response.mp3'))
            while voice_channel.is_playing():
                await asyncio.sleep(3)

        except sr.WaitTimeoutError:
            print("No speech detected within the timeout.")
            await asyncio.sleep(1)
            timeout += 1
            if timeout == 2:
                await speak_to_user(voice_channel)
                print(timeout)
                timeout = 0
            continue
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
            await asyncio.sleep(1)
            timeout += 1
            if timeout == 2:
                await speak_to_user(voice_channel)
                print(timeout)
                timeout = 0
            continue
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            await asyncio.sleep(1)
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(1)
            timeout += 1
            if timeout == 2:
                await speak_to_user(voice_channel)
                print(timeout)
                timeout = 0
                
            continue


bot.run(TOKEN)

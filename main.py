import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# Initialize recognizer & TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<Your NewsAPI Key Here>"  # still needed for news feature

# Speak function (using gTTS + pygame)
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

# AI processing using SambaNova API
def aiProcess(command):
    client = OpenAI(
        api_key="841062a1-3406-4d55-a5f7-007b109a0b1c",  # Your SambaNova key
        base_url="https://api.sambanova.ai/v1"
    )

    completion = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short, clear answers."},
            {"role": "user", "content": command}
        ],
        temperature=0.3,
        top_p=0.9
    )

    return completion.choices[0].message.content

# Command processing
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the music library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:
                speak(article['title'])
        else:
            speak("Unable to fetch news right now.")
    else:
        # Random question → SambaNova AI
        output = aiProcess(c)
        speak(output) 

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Ya")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print(f"Error: {e}")

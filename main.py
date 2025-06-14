import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame

r = sr.Recognizer()
engine = pyttsx3.init()
NEWS_API_KEY = "8e54bef0a6324c0aacd4570659b60a6d"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_slow(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def aiProcess(command):
    client = OpenAI(
        api_key="API_KEY"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
                {"role": "user", "content": command}
            ]
        )
        print(response.choices[0].message.content)
    except Exception as e:
        print("Error:", e)

def processCommand(command):
    print("Command Accepted: "+ command)
    if("open google" in command.lower()):
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif("open linkedin" in command.lower()):
        speak("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com")
    elif("open youtube" in command.lower()):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif("open facebook" in command.lower()):
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif(command.lower().startswith("play")):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        speak("Playing: "+ song)
        webbrowser.open(link)
    elif("news" in command.lower()):
        news = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}")
        if(news.status_code == 200):
            data = news.json()
            articles = data.get("articles", [])
            for article in articles:
                speak(article['title'])
        else: 
            speak("Error fetching news")
    else: 
        # Let open ai handle the request
        aiResponse = aiProcess(command)
        speak(aiResponse)


if(__name__ == '__main__'):
    speak("Initializing Jarvis....")

    while True: 
        # obtain audio from the microphone
        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening....")
                # Listen for the wake word "Jarvis"
                audio = r.listen(source, timeout=2, phrase_time_limit=2)

            print("Recognizing....")
            word = r.recognize_google(audio)
            print("Google thinks you said " + word)

            if(word.lower() == "jarvis"):
                speak("Hello There! How can i help you?")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Activated....")
                    audio = r.listen(source, timeout=2, phrase_time_limit=4)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Google could not understand audio")
        except sr.RequestError as e:
            print("Google error; {0}".format(e))


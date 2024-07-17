import speech_recognition as sr
import spacy
import os
import datetime
import pyttsx3
import webbrowser
import subprocess
from plyer import notification
from geopy.geocoders import GoogleV3
import time
import pyaudio
import requests
import base64
import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from gtts import gTTS
import schedule

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"User: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error accessing Google Speech Recognition service: {e}")
        return ""

def speak(text, rate=0.10):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def welcome_user():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    if 0 <= hour < 12:
        return "Good morning! How can I assist you today?"
    elif 12 <= hour < 14:
        return "Good afternoon! How can I assist you today?"
    elif 14 <= hour < 19:
        return "Good evening! How can I assist you today?"
    else:
        return "Good night! How can I assist you today?"

def open_spotify():
    try:
        spotify_url = "https://open.spotify.com/playlist/0T7tnjUgEwaYx8r1AiEIHG"
        spotify = webbrowser.open_new_tab(spotify_url)
        speak(f"Opening Spotify with URL: {spotify}")
        return f"Opening Spotify with URL: {spotify}"
    except Exception as e:
        print(f"Error opening Spotify: {e}")
        return "Sorry, I encountered an error while opening Spotify."

def set_skincare_reminder():
    current_time = datetime.datetime.now()
    reminder_time = current_time + datetime.timedelta(minutes=30)
    formatted_time = reminder_time.strftime("%I:%M %p")
    notification_title = "Skincare Reminder"
    notification_message = "It's time for your skincare routine!"
    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=10
    )
    speak(f"It's time for your skincare routine at {formatted_time}. Don't forget!")
    return "Setting a reminder for skincare routine. Don't forget!"

def manage_tasks():
    speak("Reading book for 30 minutes from 10 am")
    speak("Code for 60 minutes from 11 am")
    speak("Prepare for aptitude for 60 minutes from 12 pm")
    speak("Do dashboards for 30 minutes from 5 pm")

def skincare_task():
    speak("Double cleanse")
    speak("Pat toner")
    speak("Apply serum on specific concerns")
    speak("Moisturize heavily")
    speak("Protect your skin with UV shield")
    speak("Remember to exfoliate this week and apply a DIY face pack")

def Boost():
    speak("You are awesome")
    speak("Evan enna sonna namaku enna? Life goes on, bro.")
    speak("Let them be chae-bal, gae-sae-kki. It is going to be gwenchana, madhu.")

def sing_song(lyrics, voice_index=1, rate=150, pitch=50):
    song_lyrics = ["baby you light up my world like nobody else"]
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_index].id)
    engine.setProperty('rate', rate)
    engine.setProperty('pitch', pitch)
    for line in lyrics:
        engine.say(line)
        time.sleep(1)
        engine.runAndWait()

def get_weather(api_key, city_name):
    api_key = 'f12872089101d381a440c05603108002'  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric',
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            main_weather = data['weather'][0]['main']
            description = data['weather'][0]['description']
            temperature = data['main']['temp']
            weather_info = f"The weather in {city_name} is {main_weather} ({description}) with a temperature of {temperature}°C."
            return weather_info
        else:
            error_message = data['message']
            return f"Error: {error_message}"
    except Exception as e:
        return f"Error: {str(e)}"

song_lyrics1 = [
    "meghamai vandhu pogiren",
    "vennila unnai thedinen",
    "yaaridam thoothu solvadhu",
    "endru naan unnai servadhu?",
    "en anbeeee en anbeee",
    "urangamale ularal varum idhu dhano aarambam",
    "if you want to hear more I shall play in Spotify with your prompt,",
    "since I don't want to spoil Thalapathy's hit song."
]

def sing_song1(lyrics, output_path="output.mp3", lang="en"):
    full_lyrics = " ".join(lyrics)
    tts = gTTS(text=full_lyrics, lang=lang, slow=True)
    tts.save(output_path)
    os.system(f"start {output_path}")

def open_folder(folder_path):
    if os.path.exists(folder_path):
        subprocess.Popen(['explorer', folder_path])
    else:
        print(f"The folder '{folder_path}' does not exist.")

def read_notepad_file(file_path):
    if os.path.exists(file_path):
        subprocess.Popen(['notepad', file_path])
        time.sleep(2)
        with open(file_path, 'r') as file:
            content = file.read()
            speak(f"The content of the Notepad file is: {content}")
    else:
        print(f"The file '{file_path}' does not exist.")

class ReminderSystem:
    def handle_reminder_request(self):
        reminder = input("What would you like to be reminded about? ")
        speak("What would you like to be reminded about?")
        time_str = input("When should I remind you? (Format: HH:MM) ")
        try:
            hour, minute = map(int, time_str.split(':'))
            reminder_time = datetime.time(hour, minute)
            current_time = datetime.datetime.now().time()
            if current_time > reminder_time:
                reminder_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), reminder_time)
            else:
                reminder_time = datetime.datetime.combine(datetime.date.today(), reminder_time)
            print(f"Reminder set: {reminder} at {reminder_time.strftime('%H:%M')}")
            self.schedule_reminder(reminder, reminder_time)
        except ValueError:
            print("Invalid time format. Please use HH:MM format.")

    def schedule_reminder(self, reminder, reminder_time):
        now = datetime.datetime.now()
        delta = (reminder_time - now).total_seconds()
        print(f"Scheduled reminder: {reminder} at {reminder_time.strftime('%H:%M')}. Time remaining: {delta} seconds.")
        speak(f"Scheduled reminder: {reminder} at {reminder_time.strftime('%H:%M')}. Time remaining: {delta} seconds.")
        time.sleep(delta)
        print(f"REMINDER: {reminder}!")

    def daily_reset(self):
        self.reminders = []

    def check_reminders(self):
        now = datetime.datetime.now().time()
        for reminder, time in self.reminders:
            if now.hour == time.hour and now.minute == time.minute:
                print(f"REMINDER: {reminder}!")

    def start(self):
        while True:
            schedule.run_pending()
            self.check_reminders()
            time.sleep(10)

def text_input():
    while True:
        user_input = input("Enter your command: ").strip().lower()
        if user_input == "hello":
            speak("Greetings! I am Park Hyung Sik, your desktop assistant. How may I help you?")
        elif user_input == "exit":
            speak("Exiting. Goodbye!")
            break
        elif "date" in user_input:
            date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today's date is {date}")
        elif "time" in user_input:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {time}")
        elif "open spotify" in user_input:
            speak("Opening Spotify")
            open_spotify()
        elif "skin" in user_input:
            speak("Make your skin glow just like your dream")
            speak(set_skincare_reminder())
        elif "task" in user_input:
            speak("Padikira valiya paaru nuthead", rate=0.25)
            manage_tasks()
        elif "i feel low" in user_input:
            Boost()

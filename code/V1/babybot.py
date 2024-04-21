import speech_recognition as sr
import pyttsx3
import openai
import time
import RPi.GPIO as GPIO
import pygame


tts = pyttsx3.init()

GPIO.setmode(GPIO.BCM)
ATTACHED = 16
LED_PIN = 26
GPIO.setup(ATTACHED,GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

voices = tts.getProperty('voices')
openai.api_key = 'sk'

recognizer = sr.Recognizer()

tts = pyttsx3.init()

def listen(timeout=1):
    with sr.Microphone() as source:
        print("Listening...")
        #recognizer.dynamic_energy_threshold = False
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=4)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.WaitTimeoutError:
            speak("Timeout: No speech detected.")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
            return ""
        except sr.RequestError as e:
            speak(f"Speech recognition request error: {e}")
            return ""

def speak(text):
    tts.say(text)
    tts.runAndWait()

def chat(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()


def play_audio(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error:
        print("Error playing audio")

audio_file_path = "howdeep.mp3"

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED for listening
        user_input = listen(timeout=1)

        if not user_input:
            GPIO.output(LED_PIN, GPIO.LOW) 
            continue

        GPIO.output(LED_PIN, GPIO.LOW) 

        print(user_input)
        print(user_input.lower())
        listit = user_input.lower()
        listfin = listit.split()
        print(listfin, user_input)

        # Check if any word in the input is present in the valid words list
        if any(word in listfin for word in ["light", "on", "off", "play", "song", "how", "deep", "is", "your", "love", "led", "switch", "turn", "chandrayaan 3" , "chandrayan 3", "chandrayaan", "chief minister", "tamil", "nadu","tamil nadu","chief minister of tamil nadu"]):
            print("One or more valid words present")

            if any(phrase in listit for phrase in ["play", "play a song", "play how deep", "how deep is your love", "play how deep is your love", "play song", "play love"]):
                print("SONG")
                try:
                    play_audio(audio_file_path)
                except KeyboardInterrupt:
                    pygame.mixer.music.stop()  # Stop the song gracefully
                    print("Song stopped")
                    speak("Song stopped")
            elif any(phrase in listit for phrase in ["light on", "turn the light on", "turn it on", "switch on the light","light must be on"]):
                print("LIGHT ON")
                GPIO.output(ATTACHED, GPIO.HIGH)
            elif any(phrase in listit for phrase in ["light off", "turn the light off","turn the light of", "turn it off", "turn it of", "switch off the light","light must be off"]):
                print("LIGHT OFF")   
                GPIO.output(ATTACHED,GPIO.LOW)
            elif any(phrase in listit for phrase in ["what" , "is the chandrayaan 3 " , "what do you know about chandrayaan 3", " is the chandrayan 3" , "what do you know about chandrayan 3", "give me data on chandrayan 3", "give me data on chandrayaan 3", " data on","information on" , "when did the","takeoff"]):
                speak("Chandrayaan-3 is the third mission in the Chandrayaan programme, a series of lunar-exploration missions developed by the Indian Space Research Organisation. Launched in July 2023, the mission consists of a lunar lander named Vikram and a lunar rover named Pragyan, similar to those launched aboard Chandrayaan-2 in 2019. Chandrayaan-3 was launched from Satish Dhawan Space Centre on 14 July 2023. The spacecraft entered lunar orbit on 5 August, and the lander touched down in the lunar south polar region on 23 August at 12:33 UTC, making India the fourth country to successfully land on the Moon, and the first to do so near the lunar south pole.")
            elif any(phrase in listit for phrase in ["when" , "chandrayan 3", "chandraayan 3", "land", "when did the chandrayaan 3 land" , "when did the chandrayaan 3 land"]):
                #print("LIGHT OFF")   
                #GPIO.output(ATTACHED,GPIO.LOW)
                speak("The Chandrayaan 3 was launched aboard the Vikram lander on 14th july 2023 and it touched down on 23 August at 6 03 PM Indian time.")
            elif any(phrase in listit for phrase in ["who is the cm of tamil nadu", "cm of tamil nadu", "Chief minister of tamil nadu" , "chief minister of TN", "who is the chief minister of tn", "the chief minister of tamil nadu"]):
                print("CM")
                speak("The CM Of Tamil Nadu is MK Stalin")
                # PIO.output(ATTACHED, GPIO.HIGH)
            else:
                response = chat(user_input)
                speak(response)
        else:
            response = chat(user_input)
            speak(response)
        time.sleep(2)

except KeyboardInterrupt:
   GPIO.output(LED_PIN,GPIO.LOW)
   GPIO.output(ATTACHED,GPIO.LOW)
   print("over")

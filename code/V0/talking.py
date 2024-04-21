import speech_recognition as sr
import pyttsx3
import openai
import time
import RPi.GPIO as GPIO


tts = pyttsx3.init()

GPIO.setmode(GPIO.BCM)
LED_PIN = 21
GPIO.setup(LED_PIN, GPIO.OUT)

# Get the list of available voices
voices = tts.getProperty('voices')

# Print the available voices
for voice in voices:
    print(f"Voice: {voice.id}, Language: {voice.languages}, Gender: {voice.gender}")

# Set the desired voice
voice_id = "desired_voice_id"  # Replace with the ID of the desired voice
tts.setProperty('voice', voice_id)
# Set up your OpenAI API key
openai.api_key = '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'

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
tts = pyttsx3.init()

def listen(timeout=3):
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source, timeout=timeout)
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


# Define a function to send a message to the chat model and get a response
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


# Start the conversation loop
try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED for listening
        # Listen to the user's speech and convert it to text with a timeout of 20 seconds
        user_input = listen(timeout=3)

        # If there was no input, continue to listen
        if not user_input:
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn off the LED if no input
            continue

        GPIO.output(LED_PIN, GPIO.LOW)  # Turn off the LED before speaking
        # Pass the user's input to the chat model and get a response
        response = chat(user_input)

        # Speak the response using text-to-speech
        speak(response)

        # Add a delay before listening again
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.output(LED_PIN,GPIO.LOW)
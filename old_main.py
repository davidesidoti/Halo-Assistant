import threading
import datetime
import random

import speech_recognition
import pyttsx3 as tts

from neuralintents import GenericAssistant

ttsActive = False
sttActive = False

# This code initializes a speech recognition engine using the `speech_recognition` library. It sets
# the `dynamic_energy_threshold` to `True`, which allows the engine to adjust the energy threshold
# dynamically based on the ambient noise level. It sets the `pause_threshold` to 2 seconds, which is
# the amount of silence required to mark the end of a phrase. It sets the `phrase_threshold` to 0.1
# seconds, which is the minimum length of a phrase. It sets the `non_speaking_duration` to 2 seconds,
# which is the amount of silence required to mark the end of an utterance.
if sttActive:
    recognizer = speech_recognition.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 2
    recognizer.phrase_threshold = 0.1
    recognizer.non_speaking_duration = 2

# This code initializes a text-to-speech engine using the Microsoft Speech API (sapi5) driver. It sets
# the speaking rate to 150 words per minute and selects the second voice from the available voices in
# the engine.
if ttsActive:
    speaker = tts.init(driverName='sapi5')
    speaker.setProperty("rate", 150)
    speaker.setProperty("voice", speaker.getProperty('voices')[1].id)


def speak(text: str) -> None:
    """
    The function "speak" takes a string argument and uses text-to-speech to say it out loud if the
    "ttsActive" variable is True.

    @param text: str - This parameter expects a string as input, which will be the text that needs to be
    spoken out loud
    @type text: str
    """
    if ttsActive:
        speaker.say(text)
        speaker.runAndWait()
    else:
        print(f"Nova: {text}")


def get_the_time():
    """
    This Python function generates a random response with the current time included.
    """
    responses = [
        "The time is %%.",
        "It is currently %%.",
        "The current time is %%.",
        "It's approximately %%.",
        "Let me check... the time now is %%.",
        "I have the time, it's %%."
    ]

    # Get the current time
    now = datetime.datetime.now().strftime("%H:%M")

    response = random.choice(responses).replace("%%", now)
    speak(response)


# Initiate the model
methods_mapping = {
    "time": get_the_time
}
assistant = GenericAssistant(
    "./datasets/intents.json", intent_methods=methods_mapping, model_name="./models/nova_ai")

# This code block is attempting to load a pre-trained model for the `GenericAssistant` object named
# `assistant`. If the model is not found or fails to load, it will train a new model using the dataset
# specified in `./datasets/intents.json` and save the newly trained model to `./models/nova_ai`. This
# ensures that the `assistant` object has a trained model to use for processing user input and
# generating responses.
try:
    assistant.load_model()
except:
    assistant.train_model()
    assistant.save_model()


def run_assistant():
    done = False
    while not done:
        try:
            text = None
            if not sttActive:
                text = input("Enter a message: ")
            else:
                with speech_recognition.Microphone() as mic:
                    print("Mic active.")
                    audio = recognizer.listen(mic)
                    print("audio captured")

                    text = recognizer.recognize_google(audio)
                    text = text.lower()

                    print("before awake word")
                    if "nova" in text:
                        print("nova activated. Speak now...")
                        audio = recognizer.listen(mic)
                        print("audio captured after nova activated")
                        text = recognizer.recognize_google(audio)
                        text = text.lower()
                    print("after awake word")

            if text == "stop":
                speak("Bye!")
                if ttsActive:
                    speaker.stop()
                exit()
            else:
                if text is not None:
                    response = assistant.request(text)
                    if response is not None:
                        speak(response)
        except Exception as e:
            print("An error occurred: ", str(e))
            continue


run_assistant()

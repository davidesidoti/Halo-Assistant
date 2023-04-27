import datetime
import random
import os

import speech_recognition
import pyttsx3 as tts

from neuralintents import GenericAssistant


class NovaAI:
    ttsActive = True
    sttActive = True
    recognizer = None
    speaker = None
    assistant = None

    def __init__(self, ttsActive: bool = True, sttActive: bool = True) -> None:
        self.ttsActive = ttsActive
        self.sttActive = sttActive

        # This code initializes a speech recognition engine using the `speech_recognition` library. It sets
        # the `dynamic_energy_threshold` to `True`, which allows the engine to adjust the energy threshold
        # dynamically based on the ambient noise level. It sets the `pause_threshold` to 2 seconds, which is
        # the amount of silence required to mark the end of a phrase. It sets the `phrase_threshold` to 0.1
        # seconds, which is the minimum length of a phrase. It sets the `non_speaking_duration` to 2 seconds,
        # which is the amount of silence required to mark the end of an utterance.
        if self.sttActive:
            self.recognizer = speech_recognition.Recognizer()
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 2
            self.recognizer.phrase_threshold = 0.1
            self.recognizer.non_speaking_duration = 2

        # This code initializes a text-to-speech engine using the Microsoft Speech API (sapi5) driver. It sets
        # the speaking rate to 150 words per minute and selects the second voice from the available voices in
        # the engine.
        if self.ttsActive:
            self.speaker = tts.init(driverName='sapi5')
            self.speaker.setProperty("rate", 150)
            self.speaker.setProperty(
                "voice", self.speaker.getProperty('voices')[1].id)

        # Initiate the model
        methods_mapping = {
            "time": self.get_the_time,
            "model_training": self.model_train
        }
        self.assistant = GenericAssistant(
            "./datasets/intents.json", intent_methods=methods_mapping, model_name="./models/nova_ai")

        # This code block is attempting to load a pre-trained model for the `GenericAssistant` object named
        # `assistant`. If the model is not found or fails to load, it will train a new model using the dataset
        # specified in `./datasets/intents.json` and save the newly trained model to `./models/nova_ai`. This
        # ensures that the `assistant` object has a trained model to use for processing user input and
        # generating responses.
        try:
            self.assistant.load_model()
        except:
            self.assistant.train_model()
            self.assistant.save_model()

        self.run_assistant()

    def model_train(self):
        """
        This function performs self-training of a model, removes previous model files, trains the model,
        saves the new model, and notifies the user when self-training is complete.
        """
        self.speak("Starting self-training...")
        os.remove("./models/nova_ai.h5")
        os.remove("./models/nova_ai_classes.pkl")
        os.remove("./models/nova_ai_words.pkl")
        self.assistant.train_model()
        self.assistant.save_model()
        self.speak("Self-training complete!")

    def speak(self, text: str) -> None:
        """
        The function "speak" takes a string argument and uses text-to-speech to say it out loud if the
        "ttsActive" variable is True.

        @param text: str - This parameter expects a string as input, which will be the text that needs to be
        spoken out loud
        @type text: str
        """
        if self.ttsActive:
            self.speaker.say(text)
            self.speaker.runAndWait()
        else:
            print(f"Nova: {text}")

    def get_the_time(self):
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
        self.speak(response)

    def run_assistant(self):
        """
        This is a Python function for a coding assistant that uses speech recognition and text-to-speech
        to respond to user input.
        """
        done = False
        while not done:
            try:
                text = None
                if not self.sttActive:
                    text = input("Enter a message: ")
                else:
                    with speech_recognition.Microphone() as mic:
                        print("Mic active.")
                        audio = self.recognizer.listen(mic)
                        print("audio captured")

                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()

                        print("before awake word")
                        if "nova" in text:
                            print("nova activated. Speak now...")
                            audio = self.recognizer.listen(mic)
                            print("audio captured after nova activated")
                            text = self.recognizer.recognize_google(audio)
                            text = text.lower()
                        print("after awake word")

                if text == "stop":
                    self.speak("Bye!")
                    if self.ttsActive:
                        self.speaker.stop()
                    exit()
                else:
                    if text is not None:
                        response = self.assistant.request(text)
                        if response is not None:
                            self.speak(response)
            except Exception as e:
                print("An error occurred: ", str(e))
                continue


NovaAI(True, True)

import threading
import datetime
import random

import speech_recognition
import pyttsx3 as tts

from neuralintents import GenericAssistant


class Nova:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init(driverName='sapi5')
        self.speaker.setProperty("rate", 150)
        self.speaker.setProperty(
            "voice", self.speaker.getProperty('voices')[1].id)

        self.assistant = GenericAssistant(
            "datasets/intents.json", intent_methods={"time": self.get_the_time})
        self.assistant.train_model()

        # threading.Thread(target=self.run_assistant).start()
        self.run_assistant()

    def get_the_time(self):
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
        self.speaker.say(response)
        self.speaker.runAndWait()

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    print("Mic active.")
                    self.recognizer.pause_threshold = 1
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    print("before awake word")
                    # Nova
                    if "nova" in text:
                        print("nova activated. Speak now...")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("Bye!")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    print(response)
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                    else:
                        print("Text: ", text)
                    print("after awake word")
            except Exception as e:
                print("An error occurred: ", str(e))
                continue


Nova()

from neuralintents import GenericAssistant


def function_for_time():
    print("You triggered the time intent!")
    # Some action you want to take


mappings = {'time': function_for_time}

assistant = GenericAssistant(
    './datasets/intents.json', intent_methods=mappings, model_name="./models/nova_ai")

try:
    assistant.load_model()
except:
    assistant.train_model()
    assistant.save_model()


done = False

while not done:
    message = input("Enter a message: ")
    if message == "STOP":
        done = True
    else:
        print(assistant.request(message))

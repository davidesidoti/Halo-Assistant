import openai

openai.api_key = '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'


def get_response(messages: list):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.0  # 0.0 - 2.0
    )
    return response.choices[0].message


if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a virtual assistant called Nova. You will understand what the user wants to do and format everything as a json string."}
    ]
    try:
        while True:
            user_input = input("\nYou: ")
            messages.append({"role": "user", "content": user_input})
            new_message = get_response(messages=messages)
            print(f"\nNova: {new_message['content']}")
            messages.append(new_message)
    except KeyboardInterrupt:
        print("See you!")

from httpx import ConnectError
from ollama import chat,ResponseError
from pathlib import Path
import json

# system messages(a.k.a messages to chatbot)
messages = [
    {
        "role": "system",
        "content": (
            "You are consise and experience Python Tutor"
            "Answer only to user latest question"
            "Donot reqpeat previous question unless it's asked"
            "use previous messages to generate memory and understand context"
            "Always Teach with the latest technology"
        )    
    }
]

chat_history_json = Path(__file__).parent / "Chat_history.json"

# it loads the jso nfile if it's exists..
if chat_history_json.exists():
    with open(chat_history_json,"r",encoding="utf-8") as file:
        messages = json.load(file)

while True:

    # this take the user input
    user_input = input("\nYou: ")

    # to end conversations 
    end_conversations = ["quit","end","q","bye","khatam"]
    if user_input.lower().strip() in end_conversations:
        print("Bye 🤗")
        break

    # to clear or reset the conversation history
    clear_commands = ["reset","clear"]
    if user_input.lower().strip() in clear_commands:
        messages = messages[:1]
        # to clear the json file also..
        with open(chat_history_json,"w",encoding="utf-8"):
            json.dump(messages,file,indent=4)
        print("All Conversations Data Cleared 🧹")
        continue


    # saves the user messages to keep context
    messages.append(
        {
            "role": "user",
            "content": user_input 
        }
    )

    # this helps in ai chatbot to response in chunk(one or two text) freqeuntly
    assistant_response = ''
    try:
        response = chat(model="llama3.2:latest",messages=messages,stream=True)

        print("Assistant: ",end="",flush=True)
        for chunk in response:
            content = chunk.message.content
            print(content,end='',flush=True)
            assistant_response += content
        print()

    # to counter errors..
    except ResponseError as error:
        print(f"Ollama Error: {error}")
        continue
    except ConnectError as error:
        print("Ollama Server is not running")
        continue

    # this append the reponse given by chatbot..
    messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    # this saves up 20 previous messages
    messages = [messages[0]] + messages[1:][-20:]

    # this overwirte the existing json file
    with open(chat_history_json,"w",encoding="utf-8") as file:
        json.dump(messages,file,indent=4)

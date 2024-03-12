import asyncio
import websockets
import json
from gtts import gTTS
import os
import winsound
import json
import google.generativeai as genai
import requests
genai.configure(api_key="")

headers = {
    'Cookie': 'username-localhost-8888="2|1:0|10:1707918331|23:username-localhost-8888|44:OGJjYjQ0NDE5YmQwNDk3MmEyYTUxYTkzMTk5ZTU5MDc=|624ad61f4f92214fce08e863e370475b1a74ab43fb2beee3ee51915405cd2daa"; _xsrf=2|35935094|5ddceb6c0b07f4fe3cc5b80205dff5e8|1707918331; _ga=GA1.1.1153152002.1710239017; _gid=GA1.1.2124567620.1710239017; _gat_gtag_UA_156449732_1=1; _ga_R1FN4KJKJH=GS1.1.1710243003.2.1.1710244409.0.0.0'
}
async def play_sound(file_path):
    winsound.PlaySound(file_path, winsound.SND_FILENAME)
async def connect():
    while True:
        try:
            async with websockets.connect("ws://localhost:7897/queue/join", extra_headers=headers) as ws:
                # Send the first message
                first_message = {
                    "data": ["egirltea.pth", 0.33, 0.33],
                    "event_data": None,
                    "fn_index": 12,
                    "session_hash": "vzsuonv01wh"
                }
                await ws.send(json.dumps(first_message))

                # Receive the response for the first message
                output_message = await ws.recv()
                print(output_message)

                # Send the second message
                second_message = {
                    "data": [0, "D:/New folder/speech.mp3", "", 0, None, "rmvpe", "", "", 0.75, 3, 0, 0.25, 0.33, 120],
                    "event_data": None,
                    "fn_index": 8,
                    "session_hash": "vzsuonv01wh"


                }
                await ws.send(json.dumps(second_message))

                # Receive and print the output message
                while True:
                    output_message = await ws.recv()
                    print("Received message:", output_message)  # Debug output

                    try:
                        response_data = json.loads(output_message)
                        if response_data["output"]["data"][1]["is_file"]:
                            audio_file_path = response_data["output"]["data"][1]["name"]
                            await play_sound(audio_file_path)
                    except KeyError as e:
                        print("KeyError occurred:", e)
                        print("Response data:", response_data)  # Debug output
                    
                    
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed. Reconnecting...")
            break  # Reconnect if the connection is closed

async def convert_text_to_speech(response):
    # Get user input
    user_input = response
    # CHUNK_SIZE = 1024
    # url = "https://api.elevenlabs.io/v1/text-to-speech/WyvTAHTQv6HMfQUMhDyY"

    # payload = {
    #     "model_id": "eleven_monolingual_v1",
    #     "text": user_input
    # }
    # headers = {
    #     "xi-api-key": "",
    #     "Content-Type": "application/json"
    # }

    # response = requests.request("POST", url, json=payload, headers=headers)

    # print(response.text)

    # Create a text-to-speech object
    tts = gTTS(text=user_input, lang='en', tld='co.in')

    # # Specify the file path to save the speech
    file_path = 'D:/New folder/speech.mp3'

    # # Save the speech to the specified file path
    tts.save(file_path)
    # with open('speech.mp3', 'wb') as f:
    #     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
    #         if chunk:
    #             f.write(chunk)

    print("Speech saved successfully!")
    if os.path.exists(file_path):
        await connect()

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro")

prompt = "system prompt:you will act as a GenZ friend. You will speak in a GenZ tone, and your text should be text-to-speech friendly with emotions. Do not use emojis."

async def chat_bot(user_input):
    convo = model.generate_content([prompt, user_input])
    response = convo.text
    return response

async def main():
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = await chat_bot(user_input)
        print("Bot:", response)
        await convert_text_to_speech(response)

if __name__ == "__main__":
    asyncio.run(main())
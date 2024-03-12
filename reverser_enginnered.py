import asyncio
import websockets
import json
from gtts import gTTS
import os

headers = {
}

async def connect():
    while True:
        async with websockets.connect("ws://localhost:7897/queue/join", extra_headers=headers) as ws:
            # Send the message
            message = {
                "data": ["egirltea.pth", 0.33, 0.33],
                "event_data": None,
                "fn_index": 12,
                "session_hash": "bjndcgdylz"
            }
            await ws.send(json.dumps(message))
            
            # Send the second message
            output_message = await ws.recv()
            print(output_message)
            
            second_message = {
                "data": [0, "D:/New folder/speech.mp3", "", 0, None, "rmvpe", "", "", 0.75, 3, 0, 0.25, 0.33, 120],
                "event_data": None,
                "fn_index": 8,
                "session_hash": "mix0aye78wo"
            }
            await ws.send(json.dumps(second_message))
            
            # Receive and print the output message
            # output_message = await ws.recv()
            # print(output_message)
            while True:
                try:
                    # Check if connection is open before receiving
                    if ws.open:
                        output_message = await ws.recv()
                        print(output_message)
                    else:
                        # Handle connection closed scenario (optional)
                        print("Connection closed. Reconnecting...")
                        break  # Exit the inner loop and reconnect
                except websockets.exceptions.ConnectionClosed:
                    # Handle connection closed exception (optional)
                    print("Connection closed. Reconnecting...")
                    break  # Exit the inner loop and reconnect
        break
def convert_text_to_speech():
    # Get user input
    user_input = input("Enter the text to convert to speech: ")
    
    # Create a text-to-speech object
    tts = gTTS(text=user_input, lang='en', tld='co.in')
    
    # Specify the file path to save the speech
    file_path = 'D:/New folder/speech.mp3'

    # Save the speech to the specified file path
    tts.save(file_path)

    print("Speech saved successfully!")
    if os.path.exists(file_path):
        asyncio.run(connect())
# asyncio.run(connect())
convert_text_to_speech()

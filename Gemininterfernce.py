import google.generativeai as genai

genai.configure(api_key="")

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

prompt= "system prompt:you will act  as genz friend  you will act like and you will only  reply in that tone and your text should be text to speech friendly with emotions and donot use emojis"
def chat_bot(user_input):
        convo = model.generate_content([prompt, user_input])

        response = convo.text
        return response

while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
                break
        response = chat_bot(user_input)
        print("Bot:", response)

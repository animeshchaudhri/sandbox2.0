from gtts import gTTS

user_input = input("Enter the text to convert to speech: ")

tts = gTTS(text=user_input, lang='en')

file_path = 'D:/New folder/speech.mp3'


tts.save(file_path)

print("Speech saved successfully!")
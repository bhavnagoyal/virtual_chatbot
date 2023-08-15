import openai
import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading

st.title("Walmart Assistant Chatbot")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

messages = [{"role": "system", "content": "You are a Walmart store assistant ready to help with inquiries about the store."}]

openai.api_key = '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'

response = ""

def speak(text):
    engine.say(text)
    engine.runAndWait()

def CustomChatGPT(user_input):
    global response
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": response})

def voice_interface():
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            user_input = recognizer.recognize_google(audio).lower()
            st.write("You said:", user_input)
            CustomChatGPT(user_input)
            st.write("Assistant:", response)
            speak(response)
        except sr.UnknownValueError:
            st.write("Sorry, I didn't understand that.")
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            st.write("Sorry, I'm having trouble connecting to the internet.")
            speak("Sorry, I'm having trouble connecting to the internet.")

def main():
    st.write("Click the button below and speak to the Walmart Assistant:")
    if st.button("Start Assistant"):
        threading.Thread(target=voice_interface).start()

if _name_ == '_main_':
    main()

import speech_recognition as sr
import pyttsx3
from datetime import datetime
from googlesearch import search
import random
import tkinter as tk
from tkinter import ttk

# Import ttkthemes for improved styling
from ttkthemes import ThemedStyle

def greet():
    responses = ["Hello!", "Hi there!", "Greetings!", "Hey!"]
    return random.choice(responses)

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The current time is {current_time}"

def search_web(query):
    try:
        links = list(search(query, num=1, stop=1, pause=2))
        if links:
            return f"I found this link for you: {links[0]}"
        else:
            return "Sorry, I couldn't find any relevant results."
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"

def get_date():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    return f"Today's date is {current_date}"

def thank_you_response():
    responses = ["You're welcome!", "My pleasure!", "Anytime!"]
    return random.choice(responses)

def daily_conversation_response():
    responses = [
        "How was your day?",
        "Did anything interesting happen today?",
        "Tell me about your day!",
        "Anything exciting on your agenda?"
    ]
    return random.choice(responses)

def bedtime_story():
    stories = [
        "Once upon a time, in a faraway land...",
        "There was a magical kingdom where...",
        "Let me tell you the story of a brave adventurer who...",
        "Once there was a wise old owl who lived in an enchanted forest..."
    ]
    return random.choice(stories)

def tell_joke():
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised!"
    ]
    return random.choice(jokes)

def extended_conversation_response():
    responses = [
        "Tell me about your hobbies.",
        "Have you watched any interesting movies lately?",
        "What's your favorite book?",
        "If you could travel anywhere in the world, where would you go?",
        "Do you have any plans for the weekend?",
    ]
    return random.choice(responses)

def text_to_speech(text):
    engine = pyttsx3.init(driverName='espeak')
    engine.say(text)
    engine.runAndWait()

def update_response(entry, label, recognizer, root):
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        command = recognizer.recognize_google(audio).lower()
        entry.delete(0, tk.END)
        entry.insert(0, command)

        if "quit" in command:
            response = "Goodbye! Terminating the voice assistant."
            label.config(text=response)
            text_to_speech(response)
            root.destroy()  # Terminate the GUI application
        elif "hello" in command:
            response = greet()
        elif "time" in command:
            response = get_time()
        elif "search" in command:
            query = command.replace("search", "").strip()
            response = search_web(query)
        elif "date" in command:
            response = get_date()
        elif "thank you" in command:
            response = thank_you_response()
        elif any(word in command for word in ["how are you", "your day"]):
            response = daily_conversation_response()
        elif "story" in command:
            response = bedtime_story()
        elif "joke" in command:
            response = tell_joke()
        elif "talk with me" in command:
            response = extended_conversation_response()
        else:
            response = "Sorry, I didn't understand that."

        label.config(text=response)
        text_to_speech(response)
        entry.after(1000, update_response, entry, label, recognizer, root)

    except sr.UnknownValueError:
        entry.after(1000, update_response, entry, label, recognizer, root)
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")

def main():
    recognizer = sr.Recognizer()

    root = tk.Tk()
    root.title("Voice Assistant")

    # Use ThemedStyle for improved styling
    style = ThemedStyle(root)
    style.set_theme("plastik")

    # Entry widget
    entry = ttk.Entry(root, width=50)
    entry.pack(pady=10)

    # Label widget
    label = ttk.Label(root, text="Response will appear here", wraplength=400)
    label.pack(pady=10)

    # Button to trigger voice recognition manually
    def manual_recognition():
        update_response(entry, label, recognizer, root)

    manual_button = ttk.Button(root, text="Manual Recognition", command=manual_recognition)
    manual_button.pack(pady=10)

    # Add a binding to the root window to handle closing the application
    root.bind('<Control-q>', lambda event: root.destroy())

    entry.after(1000, update_response, entry, label, recognizer, root)

    root.mainloop()

if __name__ == "__main__":
    main()

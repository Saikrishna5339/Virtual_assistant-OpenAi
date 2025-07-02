import openai
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# ==== CONFIGURE YOUR OPENAI KEY HERE ====
openai.api_key = "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"

# ==== Initialize the speech engine ====
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# ==== Speak the output ====
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ==== Get input from the user via typing ====
def get_text_input():
    return input("You (type): ")

# ==== Get input from the user via speech ====
def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You (voice):", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is not working.")
        return ""

# ==== Send the command to OpenAI GPT and get response ====
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "Sorry, I couldn't connect to AI services. Please check your API key and internet."

# ==== Main assistant loop ====
def main():
    speak("Hi! I am your AI-powered assistant.")
    mode = input("Do you want to use 'text' or 'voice' input? ").strip().lower()

    if mode not in ['text', 'voice']:
        speak("Invalid input method. Please restart.")
        return

    while True:
        if mode == 'text':
            command = get_text_input()
        else:
            command = get_speech_input()

        if not command:
            continue

        if any(exit_word in command.lower() for exit_word in ['exit', 'quit', 'stop']):
            speak("Goodbye!")
            break

        # Handle some direct commands (optional shortcut)
        if "open google" in command.lower():
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "open youtube" in command.lower():
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        
        elif "what's the time" in command.lower() or "what is the time" in command.lower():
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "what's the date" in command.lower() or "what is the date" in command.lower():
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {current_date}")

        elif "open github" in command.lower():
            speak("Opening GitHub")
            webbrowser.open("https://www.github.com")

        elif "open stack overflow" in command.lower():
            speak("Opening Stack Overflow")
            webbrowser.open("https://stackoverflow.com")

        elif "who are you" in command.lower():
            speak("I am your AI-powered virtual assistant, built using OpenAI.")

        elif "how are you" in command.lower():
            speak("I'm just a bunch of code, but I'm functioning perfectly!")

        elif "tell me a joke" in command.lower():
            joke_prompt = "Tell me a short, funny joke."
            response = ask_openai(joke_prompt)
            speak(response)

        elif "what can you do" in command.lower():
            speak("I can help you with answering questions, telling jokes, opening websites, and more. Just ask!")

        elif "search" in command.lower():
            search_query = command.lower().split("search")[-1].strip()
            if search_query:
                url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                speak(f"Searching for {search_query}")
                webbrowser.open(url)
            else:
                speak("Please specify what you want to search.")


if __name__ == "__main__":
    main()

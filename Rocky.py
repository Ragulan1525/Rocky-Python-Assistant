import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib

# Initialize the pyttsx3 engine
engine = pyttsx3.init()


def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()


def greet_user():
    """Greet the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("I'm Rocky, your personal assistant. How can I help you today?")


def listen_to_command():
    """
    Capture audio from the microphone and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm all ears... Speak now!")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            print("Got it! Let me process that...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Hmm, I didn't catch that. Could you say it again?")
            return "None"
        except sr.RequestError as e:
            print(f"Oops! There was an issue with the recognition service: {e}")
            return "None"


def send_email(recipient, content):
    """
    Send an email via Gmail.
    """
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Replace with your Gmail credentials
        server.login('youremail@gmail.com', 'your-app-password')
        server.sendmail('youremail@gmail.com', recipient, content)
        server.close()
        speak("Your email has been sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        speak("Sorry, I couldn't send the email. Please try again.")


if __name__ == "__main__":
    print("Rocky is starting up...")
    greet_user()

    while True:
        command = listen_to_command()

        if 'wikipedia' in command:
            speak("Let me look that up on Wikipedia.")
            command = command.replace("wikipedia", "")
            try:
                results = wikipedia.summary(command, sentences=2)
                speak("Here's what I found:")
                print(results)
                speak(results)
            except Exception as e:
                print(f"Error fetching Wikipedia results: {e}")
                speak("I couldn't find anything on Wikipedia.")

        elif 'open youtube' in command:
            speak("Heading over to YouTube!")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in command:
            speak("Opening Google for you.")
            webbrowser.open("https://www.google.com")

        elif 'open stack overflow' in command:
            speak("Stack Overflow is ready for your queries.")
            webbrowser.open("https://stackoverflow.com")

        elif 'play music' in command:
            music_dir = '/home/ragulan/Music'
            try:
                songs = os.listdir(music_dir)
                if songs:
                    speak("Here's some music for you.")
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    speak("Hmm, looks like there's no music in your folder.")
            except Exception as e:
                print(f"Error playing music: {e}")
                speak("Sorry, I couldn't play the music.")

        elif 'the time' in command:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {current_time}.")

        elif 'open code' in command:
            code_path = "/usr/bin/code"  # Adjust the path if needed
            try:
                os.system(f"{code_path} &")
                speak("Launching Visual Studio Code.")
            except Exception as e:
                print(f"Error opening Visual Studio Code: {e}")
                speak("Sorry, I couldn't open Visual Studio Code.")

        elif 'send email' in command:
            try:
                speak("Who should I email?")
                recipient = "raguulan@gmail.com"  # Adjust recipient's email
                speak("What's the message?")
                email_content = listen_to_command()
                send_email(recipient, email_content)
            except Exception as e:
                print(f"Error sending email: {e}")
                speak("I couldn't send your email. Let me know if I should try again.")

        elif 'quit' in command or 'exit' in command:
            speak("Goodbye! Take care.")
            break

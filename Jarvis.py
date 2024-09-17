import speech_recognition as sr
import pyttsx3
import wikipedia
import sounddevice as sd
import soundfile as sf  # New library to save audio as .wav
import os
 import numpy as np

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set the assistant's voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # You can change this to voices[1] for a female voice

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=5, fs=44100):
    """Record audio using sounddevice and save it as a .wav file."""
    print("Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    # Save the recording as a .wav file
    sf.write("command.wav", recording, fs)
    print("Audio recorded and saved as 'command.wav'")
    return "command.wav"

def take_command():
    """Function to recognize voice commands using Google Speech Recognition."""
    audio_file = record_audio()

    try:
        # Use the recorded audio file for recognition
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}\n")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I didn't catch that. Please say it again.")
        return None
    return command.lower()

def main():
    """Main function to process commands."""
    speak("Hello, how can I assist you today?")

    while True:
        command = take_command()

        if command:
            if "wikipedia" in command:
                speak("Searching Wikipedia...")
                command = command.replace("wikipedia", "")
                result = wikipedia.summary(command, sentences=2)
                print(result)
                speak(result)

            elif "your name" in command:
                speak("My name is Jarvis.")

            elif "open notepad" in command:  # Opening Notepad on Windows
                speak("Opening Notepad")
                os.system("notepad.exe")

            elif "done" or "stop" in command:
                speak("Goodbye!")
                break

            else:
                speak("I am not sure how to do that yet.")

if __name__ == "__main__":
    main()

from gtts import gTTS
import speech_recognition as sr
import os
from openai import OpenAI
from io import BytesIO # For in-memory file operations
import pygame # For playing audio
import re # For text processing

# Initialize Pygame mixer
pygame.mixer.init()

# Configure the OpenAI client to point to the local Ollama server
# Ollama typically runs on http://localhost:11434
# An API key is not strictly needed for local Ollama, but the library might expect a non-empty string.
client = OpenAI(
    base_url="http://localhost:11434/v1", # Ollama's OpenAI-compatible API endpoint
    api_key="ollama" # Placeholder API key for Ollama
)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # r.adjust_for_ambient_noise(source, duration=1) # Optional: to calibrate for ambient noise
        try:
            # Timeout and phrase_time_limit can be added for when the user stops speaking
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing audio...")
            text = r.recognize_google(audio, language='en-US') # Kept as English
            print(f"You said: {text}")
            return text.lower()
        except sr.WaitTimeoutError: # If the user doesn't speak within the timeout
            print("Timeout: You didn't say anything.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service; {e}")
            return None

def speak(text):
    if not text: # If the text is empty, don't try to speak
        print("No text to speak.")
        return
    try:
        print(f"Speaking: {text}")
        tts = gTTS(text=text, lang='en', slow=False) # Kept as English
        
        # Write to an in-memory buffer instead of saving to a file
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0) # Go to the beginning of the file-like object
        
        # Load and play the audio from memory using Pygame
        pygame.mixer.music.load(mp3_fp, 'mp3') # The second argument specifies the format
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10) # Small delay to prevent high CPU usage
            
    except Exception as e:
        print(f"An error occurred during speech synthesis: {e}")

def clean_response(text):
    """Attempts to clean 'thinking' parts from the model's response."""
    # Remove text within <think> ... </think> tags
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Remove text within square brackets (e.g., [Thinking...])
    text = re.sub(r'\[.*?\]', '', text)
    # Remove text within asterisks (e.g., *after some thought*)
    text = re.sub(r'\*.*?\*', '', text)
    
    # Remove common "thinking" or "internal state" phrases
    common_thinking_phrases = [
        "Hmm,", "One moment,", "Thinking...", "Now I understand,", "Well,", "Okay,",
        "Let me think...", "I see.", "Alright,"
    ]
    for phrase in common_thinking_phrases:
        text = re.sub(r'(?i)\b' + re.escape(phrase) + r'\b\s*', '', text)

    return text.strip() # Clean up leading/trailing whitespace

def process_input_with_ollama(text, model_name): # Renamed for clarity
    if not text: # If the input text is empty
        return "Please say something."
    try:
        system_message = (
            "You are a helpful assistant. Provide direct and clear answers to the user's questions. "
            "Do not include your thinking process or internal monologues in your responses. "
            "Only produce speech text intended for the end-user."
        )
        completion = client.chat.completions.create(
            model=model_name, # Use the model name specified by the user (must be available in Ollama)
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=150
            # stream=False # Ollama by default might stream, ensure you get a complete response if not handled
        )
        raw_response_text = completion.choices[0].message.content.strip()
        
        # Clean the response before speaking
        cleaned_response_text = clean_response(raw_response_text)
        
        return cleaned_response_text
    except Exception as e:
        print(f"Error while getting response from Ollama: {e}")
        return "Sorry, I encountered a problem and couldn't generate a response."

if __name__ == '__main__':
    # Get the model name from the user at startup
    # This model must be available in your local Ollama instance (e.g., via 'ollama pull llama3')
    selected_model_name = input("Please enter the name of the Ollama model you want to use (e.g., llama3, mistral): ")
    if not selected_model_name:
        print("No model name entered. Please ensure you have a model available in Ollama.")
        # You might want to assign a default model name here or exit the program.
        # For example: selected_model_name = "llama3" 
        exit("Exiting: No model name provided.")


    print(f"Using Ollama model: {selected_model_name}")

    try:
        while True:
            print("\nSay 'assistant' to activate or 'exit program' to terminate...")
            command = listen()

            if command is None:
                continue

            if "assistant" in command:
                speak("Listening")
                input_text = listen()
                if input_text:
                    response_text = process_input_with_ollama(input_text, selected_model_name)
                    print(f"Assistant: {response_text}")
                    if response_text: 
                        speak(response_text)
                    else:
                        speak("I didn't find any content to voice in my response.")
                else:
                    speak("I didn't catch that.")
                    
            elif "exit program" in command:
                print("Exiting program...")
                speak("Exiting program...")
                break
    finally:
        pygame.mixer.quit()
        print("Pygame mixer closed.")


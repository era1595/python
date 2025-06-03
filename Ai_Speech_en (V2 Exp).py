from gtts import gTTS
import speech_recognition as sr
import os
from openai import OpenAI
from io import BytesIO # For in-memory file operations
import pygame # For playing audio
import re # For text processing
import sys

# Initialize Pygame mixer
pygame.mixer.init()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # r.adjust_for_ambient_noise(source, duration=1) # Optional: to calibrate for ambient noise
        try:
            # Timeout and phrase_time_limit can be added for when the user stops speaking
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing sound...")
            text = r.recognize_google(audio, language='en-US') # Changed to English
            print(f"You said: {text}")
            return text.lower()
        except sr.WaitTimeoutError: # If the user doesn't speak within the timeout
            print("Timeout: You didn't say anything.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
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
        tts = gTTS(text=text, lang='en', slow=False) # Changed to English

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
    pattern = r"<think>.*?</think>"
    yeni_metin = re.sub(pattern, "", text, flags=re.DOTALL)
    return yeni_metin

def process_input_with_lm_studio(text, model_name): # model_name parameter added
    if not text: # If the input text is empty
        return "Please say something."
    try:
        # Updated system message: Clearer instructions
        system_message = ("You are a helpful assistant. Provide direct and clear answers to the user's questions. ")
        completion = client.chat.completions.create(
            model=model_name, # Using the model name provided by the user
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=500
        )
        raw_response_text = completion.choices[0].message.content.strip()

        # Clean the response before speaking
        cleaned_response_text = clean_response(raw_response_text)

        return cleaned_response_text
    except Exception as e:
        print(f"Error getting response from LM Studio: {e}")
        return "Sorry, I encountered a problem and could not generate a response."

def process_input_with_ollama(text, model_name): # Renamed for clarity
    if not text: # If the input text is empty
        return "Please say something."
    try:
        system_message = ("You are a helpful assistant. Provide direct and clear answers to the user's questions. ")
        completion = client.chat.completions.create(
            model=model_name, # Use the model name specified by the user (must be available in Ollama)
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=500
            # stream=False # Ollama by default might stream, ensure you get a complete response if not handled
        )
        raw_response_text = completion.choices[0].message.content.strip()

        # Clean the response before speaking
        cleaned_response_text = clean_response(raw_response_text)

        return cleaned_response_text
    except Exception as e:
        print(f"Error getting response from Ollama: {e}")
        return "Sorry, I encountered a problem and could not generate a response."

ols=input("Which provider would you like to use (Ollama/LMStudio)")
ols.upper()
if ols=="LMSTUDİO" or "LMSTUDIO": # User might type LMSTUDIO or LMSTUDİO, so we keep both. The prompt is English.
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    if __name__ == '__main__': # Good practice to protect the main code block
        # Get the model name from the user at startup
        selected_model_name = input("Please enter the name of the model you want to use in LM Studio (e.g., lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF): ")
        if not selected_model_name:
            print("Model name not entered. Please ensure a model is loaded in LM Studio or specify a default.")
            # You might want to assign a default model name here or exit the program.
            # For example: selected_model_name = "lmstudio-community/DeepSeek-R1-Distill-Qwen-1.5B-GGUF"
            # Or: exit()

        print(f"Model used: {selected_model_name}")

        try:
            while True:
                print("\nSay 'assistant' to activate or 'exit program' to terminate...")
                command = listen()

                if command is None:
                    continue

                if "assistant" in command:
                    speak("Listening")
                    while True:
                        input_text = listen()
                        if "end conversation" in command: # Changed from "konuşmayı sonlandır"
                            print("Conversation ended, you can start a new conversation by saying assistant.")
                            speak("Conversation ended, you can start a new conversation by saying assistant.")
                            break
                        elif input_text and "exit program" in input_text: # Check for "exit program" within conversation
                            print("Exiting program...")
                            speak("Exiting program...")
                            sys.exit()
                        elif input_text:
                            response_text = process_input_with_lm_studio(input_text, selected_model_name) # Corrected to use lm_studio function
                            print(f"Assistant: {response_text}")
                            if response_text:
                                cleaned_response_text=clean_response(response_text) # Corrected variable name
                                speak(cleaned_response_text) # speak the cleaned response
                            else:
                                speak("I could not find any content to voice in my response.")
                        # Removed redundant "programdan çık" check here as it's covered by the main loop's "exit program"
                        else:
                            # speak("Sorry, I couldn't understand what you said.") # Already handled by listen()
                            pass


                elif "exit program" in command:
                    print("Exiting program...")
                    speak("Exiting program...")
                    break
        finally:
            pygame.mixer.quit() # Properly close the pygame mixer when the program ends
            print("Pygame mixer closed.")

elif ols=="OLLAMA":
    client = OpenAI(
    base_url="http://localhost:11434/v1", api_key="ollama")
    if __name__ == '__main__':
    # Get the model name from the user at startup
    # This model must be available in your local Ollama instance (e.g., via 'ollama pull llama3')
        selected_model_name = input("Please enter the name of the Ollama model you want to use (e.g., llama3, mistral): ")
        if not selected_model_name:
            print("Model name not entered. Please ensure an available model is in Ollama.")
            # You might want to assign a default model name here or exit the program.
            # For example: selected_model_name = "llama3"
            exit("Exiting: Model name not provided.")


        print(f"Ollama model used: {selected_model_name}")

        try:
            while True:
                print("\nSay 'assistant' to activate or 'exit program' to terminate...")
                command = listen()

                if command is None:
                    continue

                if "assistant" in command:
                    speak("Listening")
                    while True:
                        input_text = listen()
                        if "end conversation" in command: # Changed from "konuşmayı sonlandır"
                            print("Conversation ended, you can start a new conversation by saying assistant.")
                            speak("Conversation ended, you can start a new conversation by saying assistant.")
                            break
                        elif input_text and "exit program" in input_text: # Check for "exit program" within conversation
                            print("Exiting program...")
                            speak("Exiting program...")
                            sys.exit()
                        elif input_text:
                            response_text = process_input_with_ollama(input_text, selected_model_name)
                            print(f"Assistant: {response_text}")
                            if response_text:
                                cleaned_response_text=clean_response(response_text) # Corrected variable name
                                speak(cleaned_response_text) # speak the cleaned response
                            else:
                                speak("I could not find any content to voice in my response.")
                        # Removed redundant "programdan çık" check here as it's covered by the main loop's "exit program"
                        else:
                            # speak("Sorry, I couldn't understand what you said.") # Already handled by listen()
                            pass
                elif "exit program" in command:
                    print("Exiting program...")
                    speak("Exiting program...")
                    break
        finally:
            pygame.mixer.quit()
            print("Pygame mixer closed.")

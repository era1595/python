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
        print("Dinleniyor...")
        # r.adjust_for_ambient_noise(source, duration=1) # Optional: to calibrate for ambient noise
        try:
            # Timeout and phrase_time_limit can be added for when the user stops speaking
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Ses işleniyor...")
            text = r.recognize_google(audio, language='tr-TR') # Changed to Turkish
            print(f"Söylediğiniz: {text}")
            return text.lower()
        except sr.WaitTimeoutError: # If the user doesn't speak within the timeout
            print("Zaman aşımı: Bir şey söylemediniz.")
            return None
        except sr.UnknownValueError:
            print("Üzgünüm, ne söylediğinizi anlayamadım.")
            return None
        except sr.RequestError as e:
            print(f"Konuşma tanıma servisinden sonuç istenemedi; {e}")
            return None

def speak(text):
    if not text: # If the text is empty, don't try to speak
        print("Seslendirilecek metin yok.")
        return
    try:
        print(f"Seslendiriliyor: {text}")
        tts = gTTS(text=text, lang='tr', slow=False) # Changed to Turkish

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
        print(f"Konuşma sentezi sırasında bir hata oluştu: {e}")

def clean_response(text):
    pattern = r"<think>.*?</think>"
    yeni_metin = re.sub(pattern, "", text, flags=re.DOTALL)
    return yeni_metin

def process_input_with_lm_studio(text, model_name): # model_name parameter added
    if not text: # If the input text is empty
        return "Lütfen bir şeyler söyleyin."
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
        print(f"LM Studio'dan yanıt alınırken hata oluştu: {e}")
        return "Üzgünüm, bir sorunla karşılaştım ve yanıt oluşturamadım."

def process_input_with_ollama(text, model_name): # Renamed for clarity
    if not text: # If the input text is empty
        return "Lütfen bir şeyler söyleyin."
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
        print(f"Ollama'dan yanıt alınırken hata oluştu: {e}")
        return "Üzgünüm, bir sorunla karşılaştım ve yanıt oluşturamadım."

ols=input("Hangi sağlayıcıyı kullanmak istersiniz (Ollama/LMStudio)")
ols.upper()
if ols=="LMSTUDİO" or "LMSTUDIO":
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    if __name__ == '__main__': # Good practice to protect the main code block
        # Get the model name from the user at startup
        selected_model_name = input("Lütfen LM Studio'da kullanmak istediğiniz modelin adını girin (örn: lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF): ")
        if not selected_model_name:
            print("Model adı girilmedi. Lütfen LM Studio'da bir modelin yüklü olduğundan emin olun veya bir varsayılan belirtin.")
            # You might want to assign a default model name here or exit the program.
            # For example: selected_model_name = "lmstudio-community/DeepSeek-R1-Distill-Qwen-1.5B-GGUF"
            # Or: exit()

        print(f"Kullanılan model: {selected_model_name}")

        try:
            while True:
                print("\nEtkinleştirmek için 'asistan' deyin veya sonlandırmak için 'programdan çık' deyin...") # Changed activation word
                command = listen()

                if command is None:
                    continue

                if "asistan" in command: # New activation word ("assistant" -> "asistan")
                    speak("Dinliyorum")
                    while True:
                        input_text = listen()
                        if "konuşmayı sonlandır" in command:
                            print("Konuşma sonlandırıldı, asistan diyerek yeniden bir konuşma başlatabilirsiniz.")
                            speak("Konuşma sonlandırıldı, asistan diyerek yeniden bir konuşma başlatabilirsiniz.")
                            break
                        elif input_text:
                            response_text = process_input_with_ollama(input_text, selected_model_name)
                            print(f"Asistan: {response_text}")
                            if response_text:
                                clean_responce_text=clean_response(response_text)
                                speak(clean_response)
                            else:
                                speak("Yanıtımda seslendirilecek herhangi bir içerik bulamadım.")
                        elif input_text=="programdan çık":
                            print("Programdan çıkılıyor...")
                            speak("Programdan çıkılıyor...")
                            sys.exit()
                        else:
                            speak("Ne söylediğinizi anlayamadım.")


                elif "programdan çık" in command: # New termination command ("exit program" -> "programdan çık")
                    print("Programdan çıkılıyor...") # "Exiting program..." -> "Programdan çıkılıyor..."
                    speak("Programdan çıkılıyor...") # "Exiting program..." -> "Programdan çıkılıyor..."
                    break
        finally:
            pygame.mixer.quit() # Properly close the pygame mixer when the program ends
            print("Pygame mikseri kapatıldı.") # "Pygame mixer closed." -> "Pygame mikseri kapatıldı."

elif ols=="OLLAMA":
    client = OpenAI(
    base_url="http://localhost:11434/v1", api_key="ollama")
    if __name__ == '__main__':
    # Get the model name from the user at startup
    # This model must be available in your local Ollama instance (e.g., via 'ollama pull llama3')
        selected_model_name = input("Lütfen kullanmak istediğiniz Ollama modelinin adını girin (örn: llama3, mistral): ")
        if not selected_model_name:
            print("Model adı girilmedi. Lütfen Ollama'da kullanılabilir bir model olduğundan emin olun.")
            # You might want to assign a default model name here or exit the program.
            # For example: selected_model_name = "llama3"
            exit("Çıkılıyor: Model adı sağlanmadı.")


        print(f"Kullanılan Ollama modeli: {selected_model_name}")

        try:
            while True:
                print("\nEtkinleştirmek için 'asistan' deyin veya sonlandırmak için 'programdan çık' deyin...")
                command = listen()

                if command is None:
                    continue

                if "asistan" in command:
                    speak("Dinliyorum")
                    while True:
                        input_text = listen()
                        if "konuşmayı sonlandır" in command:
                            print("Konuşma sonlandırıldı, asistan diyerek yeniden bir konuşma başlatabilirsiniz.")
                            speak("Konuşma sonlandırıldı, asistan diyerek yeniden bir konuşma başlatabilirsiniz.")
                            break
                        elif input_text:
                            response_text = process_input_with_ollama(input_text, selected_model_name)
                            print(f"Asistan: {response_text}")
                            if response_text:
                                clean_responce_text=clean_response(response_text)
                                speak(clean_response)
                            else:
                                speak("Yanıtımda seslendirilecek herhangi bir içerik bulamadım.")
                        elif input_text=="programdan çık":
                            print("Programdan çıkılıyor...")
                            speak("Programdan çıkılıyor...")
                            sys.exit()
                        else:
                            speak("Ne söylediğinizi anlayamadım.")

                elif "programdan çık" in command: # "exit program" kelimesini Türkçe'ye çevirdim.
                    print("Programdan çıkılıyor...")
                    speak("Programdan çıkılıyor...")
                    break
        finally:
            pygame.mixer.quit()
            print("Pygame mikseri kapatıldı.")

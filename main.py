import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import MyMemoryTranslator
import random
import time

vida = 3
duration = 5  # segundos de gravação
sample_rate = 44100

print("hello")

words_by_level = {
    "facil": ["gato", "cachorro", "maçã", "leite", "sol"],
    "medio": ["casa", "escola", "amigo", "janela", "amarelo"],
    "dificil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]
}

nivel = int(input("Qual nível de dificuldade você quer? " +
"(1-facil, 2-medio, 3-dificil): "))
if nivel==1:
    dificuldade = "facil"

if nivel==2:
    dificuldade = "medio"

if nivel==3:
    dificuldade = "dificil"


palavra = random.choice(words_by_level[dificuldade])
print("Fale em ingles a palavra:", palavra)
    
print("Fale agora...")
recording = sd.rec(
int(duration * sample_rate), # o número de amostras a serem registradas
samplerate=sample_rate,      # taxa de amostras
channels=1,                  # 1 significa gravação mono
dtype="int16")               # tipo de dados para as amostras registradas
sd.wait()  # aguardando o término da gravação

wav.write("output.wav", sample_rate, recording)
print("Gravação concluída, estou reconhecendo...")
recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio, language="pt-BR")
    print("Você disse:", text)
        
    translator = MyMemoryTranslator(
        source="pt-BR",
        target="en-US"
    ).translate(text).lower
        
    print("Tradução para o inglês:", translator)
    


except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
    print("A fala não pôde ser reconhecida.")
except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
    print(f"Service error: {e}")

   
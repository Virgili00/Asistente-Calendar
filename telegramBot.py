import telebot
import os
from dotenv import load_dotenv
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
import io

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token del bot desde las variables de entorno
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Crear una instancia del bot
bot = telebot.TeleBot(TOKEN)

# Inicializar el reconocedor de voz
recognizer = Recognizer()

# Manejador para mensajes de voz
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        # Descargar el archivo de audio en memoria
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Convertir el archivo descargado (en bytes) a un buffer de memoria
        audio_bytes = io.BytesIO(downloaded_file)

        # Usar pydub para convertir el archivo de ogg a wav (en memoria)
        audio = AudioSegment.from_ogg(audio_bytes)
        wav_io = io.BytesIO()  # Crear un buffer para el archivo wav
        audio.export(wav_io, format='wav')  # Exportar como wav en memoria
        wav_io.seek(0)  # Colocar el puntero al principio del archivo de memoria

        # Usar SpeechRecognition para transcribir el audio
        with AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='es-ES')
            bot.reply_to(message, f'Transcripción: {text}')
    
    except Exception as e:
        bot.reply_to(message, f'Error al transcribir el audio: {str(e)}')

# Iniciar el bot
bot.polling()

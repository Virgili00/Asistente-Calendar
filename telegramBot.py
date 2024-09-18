import telebot
import os
from dotenv import load_dotenv
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
import io
from llm import *
from transcriptor import *
from settterCalendar import *
import json
recognizer=Recognizer()

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
class BotTelegram:
    def __init__(self):
        """Inicializa el bot con el token y configura los manejadores."""
        self.TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.bot = telebot.TeleBot(self.TOKEN)
        self.configurar_manejadores()
        self.calendar=SetterCalendar()
        self.calendar.autenticar()

    def configurar_manejadores(self):
        """Registra los diferentes manejadores de mensajes."""
        
        # Manejador para mensajes de voz
        @self.bot.message_handler(content_types=['voice'])
        def manejar_mensaje_voz(message):
            self.procesar_mensaje_voz(message)

        # Manejador para mensajes de texto
        @self.bot.message_handler(content_types=['text'])
        def manejar_mensaje_texto(message):
            self.enviarMensaje(message.chat.id, "Hola, ¡recibí tu mensaje!")

    def procesar_mensaje_voz(self, message):
        try:
            # Descargar el archivo de audio en memoria
            audioDescargado=self.descargarAudio(message)
            promt=self.transcribirAudio(audioDescargado)
            respuesta=self.obtenerRespuesta(promt)
            respuestaJson=self.convertirJson(respuesta)
            self.setCalendar(respuestaJson)
            self.bot.reply_to(message,'se guardo el evento en el calendar \n {promt} \n {respuesta}')
        except Exception as e:
            self.bot.reply_to(message, f'{str(e)}')
            print(e)

    def enviarMensaje(self, chat_id, mensaje):
        """Envía un mensaje a un chat específico."""
        try:
            self.bot.send_message(chat_id, mensaje)
        except Exception as e:
            print(f"Error al enviar el mensaje: {str(e)}")

    def iniciar_bot(self):
        """Inicia el bot y comienza a escuchar mensajes."""
        self.bot.polling(non_stop=True)
    def descargarAudio(self,message):
        file_info = self.bot.get_file(message.voice.file_id)
        audioDescargado = self.bot.download_file(file_info.file_path)
        return audioDescargado
    def transcribirAudio(self,audio:bytes):
        audioTranscripto=Transcriptor(audio).transcribir()
        return audioTranscripto
    def obtenerRespuesta(self,audioTranscripto:str):
        respuesta=LLM(audioTranscripto).invocarLlm()
        return respuesta
    def convertirJson(self,respuesta:str):
        prompt=json.loads(respuesta)
        return prompt
    def setCalendar(self,evento):
        self.calendar.setCalendar(evento)
    
# Clase o métodos adicionales para procesar otras lógicas podrían ir aquí

# Instanciar y ejecutar el bot
if __name__ == "__main__":
    bot = BotTelegram()
    bot.iniciar_bot()

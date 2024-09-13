import io
import speech_recognition as sr
from pydub import AudioSegment

class Transcriptor():
    def __init__(self,audio):
        self.audio=audio
        self.reco = sr.Recognizer()
       
        self.reco.energy_threshold = 3000
       
    
    def transcribir(self):
        audioConvertido=self.convertirAudio()
        with sr.AudioFile(audioConvertido) as fuente_audio:
            audioData = self.reco.record(fuente_audio)
            try:
                texto = self.reco.recognize_google(audioData, language='es-ES')
                return texto
            except sr.UnknownValueError:
                return "No se pudo entender el audio"
            except sr.RequestError as e:
                return f"Error al solicitar resultados de Google Speech Recognition: {e}"
        
    def convertirAudio(self):
        try:
            audioCompleto = AudioSegment.from_file(io.BytesIO(self.audio), format="ogg")
            audioWavEnMemoria = io.BytesIO()
            audioCompleto.export(audioWavEnMemoria, format="wav")
            audioWavEnMemoria.seek(0)  # Reposicionar el puntero al inicio
        except Exception as e:
            print(f'fallo la conversion{e}')

        return audioWavEnMemoria
    
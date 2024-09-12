import langchain_groq
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
import dotenv
import os
groq_api_key = os.environ['GROQ_API_KEY']
dotenv.load_dotenv()

class LLM:
    def __init__(self):
        self.llm = ChatGroq(
            model="mixtral-8x7b-32768",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2)
            # other
    def setPromt(self,promt):
        messages = [
                (
        "system",
        """sos un bot que agenda turnos, te voy a pasar un texto  y vos debes extraer la informacion del texto para agendar el turno.
        la info que necesitas es: fecha, hora y un titulo para ponerle al evento y debes devolver esa informacion extraida en formato JSON
        <Ejemplo>
        
        """,
                ),
        ("human", promt),
                    ]
        return messages
    def invocarLlm(self,promt):
        respuesta=self.llm.invoke(self.setPromt(promt))
        return respuesta.content
        
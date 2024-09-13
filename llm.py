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
import datetime
import re
groq_api_key = os.environ['GROQ_API_KEY']
dotenv.load_dotenv()

class LLM:
    def __init__(self,promt):
        self.llm = ChatGroq(
            model="llama3-70b-8192",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2)
        self.promt=promt
        self.fecha=datetime.date.today()
            
    def setPromt(self,promt):
        messages = [
                (
        "system",
        f"""
        Informacion extra
        fecha actual {self.fecha}
        Extrae los datos  y proporciona solo el JSON resultante. No incluyas ninguna nota o comentario adicional.
        respuesta ejemplo:
        
        "summary": "Reunión de ejemplo",
        "start": 
            "dateTime": "2024-09-15T10:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        ,
        "end": 
            "dateTime": "2024-09-15T11:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        
                
                )
        """,
                ),
        ("human", promt),
                    ]
        return messages
    def invocarLlm(self):
        respuesta=self.llm.invoke(self.setPromt(self.promt))
        print(respuesta.content)
        return respuesta.content
        
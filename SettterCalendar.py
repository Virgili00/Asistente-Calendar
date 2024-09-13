from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os


class SetterCalendar:
    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
        self.servicio=self.autenticar()
        
    
    def autenticar(self):
        creds=None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                            )
                creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        return build("calendar","v3",credentials=creds)
    def setCalendar(self,evento):
        
        try:
            evento = self.servicio.events().insert(calendarId='primary', body=evento).execute()
            return print("se genero con exíto")
        except Exception as e:
            return print(f'No se a podido agendar el evento{e}')
    
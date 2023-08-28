import json
from typing import Optional
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class Browser:
    
    def __sign__(self, SCOPES):
        flow = InstalledAppFlow.from_client_secrets_file('File/Credentials.json', SCOPES)
        return flow.run_local_server(port=0)
    
    def __init__(self, info: Optional[dict] = None) -> None:
        SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.addons.current.message.action', 'https://www.googleapis.com/auth/gmail.addons.current.message.metadata', 'https://www.googleapis.com/auth/gmail.addons.current.message.readonly', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly']
        if info is not None:
            self.__creds__ = Credentials.from_authorized_user_info(info, SCOPES)
            if not self.__creds__ or not self.__creds__.valid:
                if self.__creds__ and self.__creds__.expired and self.__creds__.refresh_token: self.__creds__.refresh(Request())
                else: self.__creds__ = self.__sign__(SCOPES)
        else: self.__creds__ = self.__sign__(SCOPES)
    
    @property
    def Credentials(self):
        return self.__creds__
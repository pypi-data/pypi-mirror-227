import json, base64, re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from typing import Optional
import dateutil.parser as parser

class Email:
    
    def __init__(self, creds: Credentials, From: Optional[str] = None) -> None:
        self.temp_all_email     = list()
        self.temp_from_email    = list()
        self.__user_id__        =  'me'
        self.__label_id_one__   = 'INBOX'
        self.__label_id_two__   = 'UNREAD'
        self.__service__        = build('gmail', 'v1', credentials=creds)
        UNREAD                  = True
        self.__unread_msgs__    = self.__service__.users().messages().list(userId='me', labelIds=[self.__label_id_two__]).execute().get('messages')
        if self.__unread_msgs__ is None: 
            self.__unread_msgs__    = self.__service__.users().messages().list(userId='me').execute().get('messages')
            UNREAD              = False
        for msg in self.__unread_msgs__:
            temp_dict       = dict()
            self.__txt__    = self.__service__.users().messages().get(userId='me', id=msg['id']).execute()
            payload = self.__txt__['payload']
            headers = payload['headers']
            for One in headers:
                if One['name'] == 'Subject':
                    subject = One['value']
                    temp_dict['Subject']    = subject
            for thr in headers: # getting the date
                if thr['name'] == 'Date':
                    msg_date = thr['value']
                    date_parse = (parser.parse(msg_date))
                    m_date = (date_parse.date())
                    temp_dict['Date'] = str(m_date)
            for Two in headers:
                if Two['name'] == 'From':
                    sender = Two['value']
                    temp_dict['Sender']     = sender

            temp_dict['Snippet'] = self.__txt__['snippet']
            try:
                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data)
                soup = BeautifulSoup(decoded_data , "lxml")
                body = soup.body()
                temp_dict['Message'] = decoded_data.decode()
            except Exception as e: pass
            if UNREAD: self.__service__.users().messages().modify(userId=self.__user_id__, id=msg['id'],body={ 'removeLabelIds': ['UNREAD']}).execute()
            if From is not None:
                if re.search(From.lower(), sender) or re.search(From.lower(), subject):
                    self.temp_from_email.append(temp_dict)
            self.temp_all_email.append(temp_dict)
        json.dump(self.temp_all_email, open('Email.json', 'w'), indent=4)
        json.dump(self.temp_from_email, open('Email_Specific.json', 'w'), indent=4)
    
    def __repr__(self) -> str:
        return json.dumps(self.__unread_msgs__)
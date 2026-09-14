import json
import datetime

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from ollama import chat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({"isMessage": True, "message":
                                        {"context": message, "sender": "me", "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "fromMe": True }}))
        self.send(text_data=json.dumps({"isMessage": False, "status": "thinking"}))
        response = chat(
            model='gemma4:e4b',
            messages=[
                {
                    "role": 'user',
                    'content': message,
                }
            ],
        )
        self.send(text_data=json.dumps({"isMessage": True, "message":
                                        {"context": response.message.content, "sender": "AI", "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "fromMe": False }}))
        self.send(text_data=json.dumps({"isMessage": False, "status": "wait4you"}))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))




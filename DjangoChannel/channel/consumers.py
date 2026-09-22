import json
import datetime

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, RoomMember

from ollama import chat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return
        is_member = RoomMember.objects.filter(room__id=self.room_id, member=self.user).exists()
        if not is_member:
            self.close()
            return
        self.accept()
        messages = Message.objects.filter(room__id=self.room_id)
        for message in messages:
            fromMe = True if self.user.id == message.sender.id else False
            self.send(text_data=json.dumps({"isMessage": True, "message":{"context": message.context, "sender": message.sender.username, "time": message.at_received.strftime("%Y-%m-%d %H:%M"), "fromMe": fromMe}}))
        

    def disconnect(self, close_code):
        print("disconnect:", close_code)
        raise StopConsumer()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({"isMessage": True, "message":
                                        {"context": message, "sender": self.user.username, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "fromMe": True }}))
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




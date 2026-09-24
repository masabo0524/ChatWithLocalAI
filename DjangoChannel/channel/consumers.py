import json
import datetime

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, RoomMember, ChatRoom

from ollama import chat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_instance = ChatRoom.objects.get(id=self.room_id)
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
        isAskAI = text_data_json['isAskAI']
        received_time = datetime.datetime.now()
        received_time_format = received_time.strftime("%Y-%m-%d %H:%M")
        self.send(text_data=json.dumps({"isMessage": True, "message":
                                        {"context": message, "sender": self.user.username, "time": received_time_format, "fromMe": True }}))
        received_message = Message(room=self.room_instance, at_received=received_time, sender=self.user, context=message)
        received_message.save()
        
        if(isAskAI):

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
            sending_time = datetime.datetime.now()
            sending_time_format = sending_time.strftime("%Y-%m-%d %H:%M")
            self.send(text_data=json.dumps({"isMessage": True, "message":
                                            {"context": response.message.content, "sender": "AI", "time": sending_time_format, "fromMe": False }}))
            sending_message = Message(room=self.room_instance, at_received=received_time, sender=self.user, context=response.message.content, reply_byAI=True)
            sending_message.save()
        self.send(text_data=json.dumps({"isMessage": False, "status": "wait4you"}))


    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))




from django.urls import path
import uuid

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<uuid:room_id>/", consumers.ChatConsumer.as_asgi()),
]

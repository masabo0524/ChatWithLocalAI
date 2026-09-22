from django.urls import path

from . import views

app_name = "channel"

urlpatterns = [
    path('', views.index, name="index"),
    path('room/<str:room_id>/', views.room, name="room"),
    path("rooms/", views.ListRoom.as_view(), name="roomlist"),
]

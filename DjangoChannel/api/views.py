from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = get_user_model().objects.all()

    



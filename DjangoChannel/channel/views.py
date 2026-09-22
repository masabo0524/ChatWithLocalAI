from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView as OfficialLogin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib.auth import get_user_model

from .forms import SignUpForm, LoginForm, AddRoomForm
from .models import ChatRoom, RoomMember

User = get_user_model()


def index(request):
    return render(request, "index.html")

def room(request, room_id):
    return render(request, 'room.html', {"room_id": room_id})


class HomeView(TemplateView):
    template_name = "top_page.html"


class NewRoom(LoginRequiredMixin, CreateView):
    template_name = "add_room.html"
    form_class = AddRoomForm
    success_url = reverse_lazy("channel:roomlist")

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()

            RoomMember.objects.create(
                room=self.object,
                member=self.request.user
            )

        return HttpResponseRedirect(self.get_success_url())
        


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "signup.html"
    success_url = reverse_lazy("channel:index")


class LoginView(OfficialLogin):
    form_class = LoginForm
    template_name = "login.html"
    next_page = reverse_lazy("channel:index")


class ListRoom(ListView):
    model = ChatRoom
    template_name = "chat_room.html"
    context_object_name = "rooms"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(member__member=self.request.user)
        return qs

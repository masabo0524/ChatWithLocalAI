from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.conf import settings
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('Please Enter your email')
        if not password:
            raise ValueError('Please Enter your Password')

        email = self.normalize_email(email)
        
        user = self.model(
            username=username,
            email=email,
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if not email:
            raise ValueError('Please Enter your email')
        if not password:
            raise ValueError('Please Enter your Password')

        email = self.normalize_email(email)
        
        user = self.model(
            username=username,
            email=email,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]
    

class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    room_name = models.CharField(null=False, blank=False)

    def __str__(self):
        return self.room_name


class RoomMember(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="member")
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chatroom")

    def __str__(self):
        return f"{self.room}_{self.member}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="message")
    at_received = models.DateTimeField(editable=True, null=False, blank=False)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="message")
    context = models.TextField()
    reply_byAI = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}"
    

class InvitationManager(models.Manager):

    def issueInvitation(self, user):
        self.filter(expiary_date__lt=timezone.now()).delete()
        self.filter(user=user).delete()
        expiary_date = timezone.now() + timedelta(minutes=settings.INVITATION_EXPIRE_MINUTES)
        invitation_token = self.model(user=user, expiary_date=expiary_date)
        invitation_token.save()
        return invitation_token

    def approveUser(self, token: uuid.UUID):
        try:
            invitation = self.get(token=token)
        except self.model.DoesNotExist:
            invitation.delete()
            raise ValidationError("Invalid invitation token.")

        if invitation.expiary_date < timezone.now():
            raise ValidationError("The invitation token has expired.")

        return invitation.user        


class InvitationToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="invitation")
    expiary_date = models.DateTimeField()

    objects = InvitationManager()

    def __str__(self):
        return f"{self.user}: {self.token}"

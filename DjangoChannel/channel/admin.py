from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from .models import CustomUser, ChatRoom, RoomMember, Message

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "email",
        "username",
        "birthday",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
    )

    ordering = ("email",)

    fieldsets = (
        ("Basic Information", {
            "fields": ("email", "password")
        }),
        ("Personal information", {
            "fields": ("username", "birthday")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
    )


class MemberInline(admin.TabularInline):
    model = RoomMember
    extra = 1

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

@admin.register(ChatRoom)
class ChatRoomAdmin(ModelAdmin):
    list_display = ["room_name","id",]
    search_fields = ["room_name"]
    fields = ["room_name", "id",]
    readonly_fields = ["id"]
    inlines = [MemberInline, MessageInline]

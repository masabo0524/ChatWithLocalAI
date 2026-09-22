from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import get_user_model

User = get_user_model();


class SignUpForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.save()
        return user

    
    class Meta:
        model = User
        fields = ["username", "birthday", "email"]

    
class LoginForm(AuthenticationForm):
    pass

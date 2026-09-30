from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.core.exceptions import ValidationError
from rest_framework_simplejwt import tokens as jwt_tokens

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(max_length=128, write_only=True, style={"input_type": "password"})
    
    def validate_password_not_contain_username(self, password, username):
        if username.lower() in password.lower():
            raise ValidationError("The password must not contain your username.")


    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def validate(self, data):
        try:
            self.validate_password_not_contain_username(data["password"], data["username"])
        except ValidationError as e:
            raise ValidationError(e)

        if not data["password"] == data["confirm_password"]:
            raise ValidationError("Passwords do not match.")
        
        return data

    def save(self):
        instance = User.objects.create_user(username=self.validated_data["username"],
                                            email=self.validated_data["email"],
                                            password=self.validated_data["password"],
                                            birthday=self.validated_data["birthday"],)
        return instance
    
    class Meta:
        model = User
        fields = ["username", "birthday", "email", "password", "confirm_password"]
        extra_kwargs = {
            'password': {
                'write_only': True,
                "style": {
                    "input_type": "password",
                }
            },
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        credentials = {"username": data["username"],
                       "password": data["password"]}
        self.user = authenticate(**credentials)
        if self.user is None:
            raise ValidationError("Authentication failed.")
        tokens = jwt_tokens.RefreshToken.for_user(self.user)
        print(type(tokens.access_token))
        return ()

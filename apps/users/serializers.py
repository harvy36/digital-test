from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.users.models import Member, Loan
from apps.library.models import Book
from apps.library.serializers import BookSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ["user"]


class LoanSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Loan
        fields = ["member", "book"]


class LoanDetailsSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ["member", "book"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(username=email).first()
        if user is None or not user.check_password(password):
            raise ValidationError("Correo electrónico o contraseña inválidos")

        attrs["user"] = user
        return attrs

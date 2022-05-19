from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title, User


class CategoryField(serializers.SlugRelatedField):

    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class GenreField(serializers.SlugRelatedField):

    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        required=False,
        many=True,
    )
    category = CategoryField(
        queryset=Category.objects.all(),
        slug_field="slug",
        required=False,
    )
    rating = serializers.IntegerField(
        required=False
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field="id",
        many=False,
        read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Review

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        title = get_object_or_404(
            Title,
            pk=self.context["view"].kwargs.get("title_id")
        )
        author = self.context["request"].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли обзор на данное произведение"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field="text")

    class Meta:
        fields = "__all__"
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )
        model = User

    def validate_email(self, attrs):
        if attrs == self.context["request"].user:
            raise serializers.ValidationError(
                "Такой email уже зарегистрирован!"
            )
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role",
        )
        read_only_fields = ("username", "email", "role",)


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_email(self, attrs):
        if attrs == self.context["request"].user:
            raise serializers.ValidationError(
                "Такой email уже зарегистрирован!"
            )
        return attrs

    def validate_username(self, attrs):
        if attrs == "me":
            raise serializers.ValidationError(
                'Запрещено имя "me", придумайте другое имя!'
            )
        return attrs


class TokenSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["confirmation_code"] = serializers.CharField(
            required=False
        )
        self.fields["password"] = serializers.HiddenField(default="")

    def validate(self, attrs):
        self.user = get_object_or_404(User, username=attrs["username"])
        if self.user.confirmation_code != attrs["confirmation_code"]:
            raise serializers.ValidationError("Неверный код подтверждения")
        data = str(self.get_token(self.user))

        return {"token": data}

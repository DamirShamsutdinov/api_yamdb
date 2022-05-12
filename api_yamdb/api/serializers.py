from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView

from reviews.models import Category, Genre, Title, Review, Comment, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review


class СommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_email(self, attrs):
        if attrs == self.context['request'].user:
            raise serializers.ValidationError(
                'Такой email уже зарегистрирован!')
        return attrs

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.email)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.email)
        instance.last_name = validated_data.get('last_name', instance.content)
        instance.bio = validated_data.get('bio', instance.created)
        is_superuser = self.user.is_superuser
        if not is_superuser:
            raise serializers.ValidationError('Роль юзера менять нельзя!')
        instance.role = validated_data.get('role', instance.created)
        instance.save()
        return instance

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


# class SignupView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         username = request.data['username']
#         serializer = UsersSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

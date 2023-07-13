from rest_framework import serializers, validators
from books.models import Publisher, Author, Book, Customer, MyBook, Comment
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
                'password': {'write_only': True},
                'email': {
                    "required": True,
                    "allow_blank": False,
                    "validators": [
                        validators.UniqueValidator(
                            User.objects.all(), "A user with that email already exists"
                        )
                    ]
                }
            }

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        hashed_password = make_password(password)
        user = User.objects.create(
                username = username, 
                email = email, 
                password = hashed_password
            )

        return user

class PublisherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Publisher
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    # books = BookSerializer(many=True)
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {'total_price': {'required': False} }

class BookSerializer(serializers.ModelSerializer):
    publishers = PublisherSerializer(read_only=True)
    authors = AuthorSerializer(read_only=True)
    customers = CustomerSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = '__all__'

# -------------------------------------------------------------------------
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['book']

class MyBookSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = MyBook
        fields = '__all__'
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password

from rest_framework.response import Response
from rest_framework import status


User = get_user_model()



class RegisterUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    email = serializers.EmailField(label='Email address', max_length=254, required=True)
    username = serializers.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                        max_length=150, 
                        required=True,
                        validators=[UnicodeUsernameValidator], )
                        #queryset=User.objects.all())
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, 
                                     required=True, 
                                     write_only=True)
    

    class Meta:
        model = User
        fields = ['id','email','username','first_name','last_name','password']
    
    def validate_password(self, data):
            validate_password(password=data, user=User)
            return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user



class ShowUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(method_name='get_is_subscribed')

    class Meta:
        model = User
        fields = ['id','email','username','first_name','last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        return True


class UserPasswordSerilazer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=150, required=True, write_only=True)
    current_password = serializers.CharField(max_length=150, required=True, write_only=True)


    class Meta:
        model = User
        fields = ['new_password','current_password']


    def validate_current_password(self, data):
        #TODO получать текущего пользователя
        user = User.objects.get(id=2)
        if user.check_password(data):
            return data
        else:
            raise serializers.ValidationError("Пароль не изменён, так как прежний пароль введён неправильно.") 

    def validate_new_password(self, data):
        #TODO получать текущего пользователя
        #user = User.objects.get(id=2)
        if validate_password(password=data):
            return data
        else:
            raise serializers.ValidationError("Пароль не изменён, так как новый не прошёл валидацию") 

    

    def create(self, validated_data):
        # TODO текущий пользователь
        user = User.objects.get(id=2)
        user.set_password(validated_data['new_password'])
        return Response(status=status.HTTP_202_ACCEPTED)



from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from .models import Subscription
from api.models import Recipe
from api.serializers import ShortShowReciprSerializer

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
        user = self.context.get('request').user
        try:
            tmp = Subscription.objects.get(
                respondent=user.id,
                subscriptions=obj.id
            )
        except:
            return False

        return True


class UserPasswordSerilazer(serializers.ModelSerializer):
    #user = serializers.HyperlinkedRelatedField(source='username')
    new_password = serializers.CharField(max_length=150, required=True, write_only=True)
    current_password = serializers.CharField(max_length=150, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['new_password','current_password']


    def validate_current_password(self, data):
        request = self.context.get('request')
        user = request.user
        if user.check_password(data):
            return data
        else:
            raise serializers.ValidationError("Пароль не изменён, так как прежний пароль введён неправильно.") 

    def validate_new_password(self, data):
        validate_password(password=data, user=User)
        return data


    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['new_password'])
        return Response(status=status.HTTP_202_ACCEPTED)



class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ('email', 
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'is_subscribed', 
            'recipes', 
            'recipes_count',
            )

    def give_kwargs(self, name):
        source = self.context.get('request').__dict__['parser_context']['kwargs'][name]
        return source

    def give_list_kwargs(self):
        return self.context.get('request').__dict__['parser_context']['kwargs']


    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        user_check = obj
        try:
            subscript = Subscription.objects.get(respondent=user,
                                                 subscriptions=user_check)
        except:
            return False

        return True


    def get_recipes(self, obj):
        user_check = obj
        recipe = Recipe.objects.filter(author=user_check).all()
        serializer = ShortShowReciprSerializer(recipe, many=True)
        return serializer.data



    def get_recipes_count(self, obj):
        user_check = obj
        recipe = Recipe.objects.filter(author=user_check).all().count()
        return recipe


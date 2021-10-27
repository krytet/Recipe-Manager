import re
from django.http.response import HttpResponse
import requests
from rest_framework import mixins, status
from rest_framework.generics import DestroyAPIView
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.views import APIView
from . import serializers, models
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken

User = get_user_model()


class CustomObtainAuthToken(APIView):
    serializer_class = serializers.CustomAuthTokenSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        print('!!!!!!!!!!!!!!!!!!!!!!!')
        print(user)
        token, created = Token.objects.get_or_create(user=user)
        print()
        

        return Response({'auth_token': token.key})


class CustomDeleteAuthToken(APIView):
    permission_classes = (permissions.IsAuthenticated,)



    def post(self, request, *args, **kwargs):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        user = request.user
        print(user)
        token = Token.objects.get(user=user) 
        token.delete()
        return Response(status=status.HTTP_201_CREATED)





class RecipeView(ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer


class TagView(mixins.RetrieveModelMixin,
              #mixins.CreateModelMixin,
              mixins.ListModelMixin,
              GenericViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer

def Se(request):
    return HttpResponse('Hi ')
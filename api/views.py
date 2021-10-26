from django.http.response import HttpResponse
from rest_framework.serializers import ModelSerializer
from . import serializers, models
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeView(ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer


class TagView(ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer

def Se(request):
    return HttpResponse('Hi ')
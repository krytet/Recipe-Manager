import os
from django.db.models.deletion import PROTECT
from django.http.response import FileResponse, HttpResponse
from rest_framework import mixins, status
from rest_framework.generics import DestroyAPIView, ListAPIView, get_object_or_404
from rest_framework.views import APIView
from . import serializers, models
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from tempfile import TemporaryFile


User = get_user_model()


class CustomObtainAuthToken(APIView):
    serializer_class = serializers.CustomAuthTokenSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    # Получение токена пользователя
    def post(self, request, *args, **kwargs):
        serializer = serializers.CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key})


class CustomDeleteAuthToken(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # Удаление токена пользователя
    def post(self, request, *args, **kwargs):
        user = request.user
        token = Token.objects.get(user=user) 
        token.delete()
        return Response(status=status.HTTP_201_CREATED)


# CRUD операций над рецептом
class RecipeView(ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer


# Получение Тегов
class TagView(mixins.RetrieveModelMixin,
              mixins.ListModelMixin,
              GenericViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


# Получение ингридиентов
class IngerdientViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer



class FavoriteViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    # добавить в список изброных
    def retrieve(self, request, *args, **kwargs):
        recipe = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
        favorite, status_ = models.FavoriteRecipe.objects.get_or_create(
            person=request.user,
            recipe=recipe,
        )
        if status_:
            serializer = serializers.ShortShowReciprSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = {
                'errors': 'Данный рецеп уже добавлен в избраное'
            }
            return Response(error ,status=status.HTTP_400_BAD_REQUEST)


    #Удалить из списка изброных
    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
        try:
            tmp = models.FavoriteRecipe.objects.get(
                person=request.user,
                recipe=recipe,
            )
            tmp.delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


    #Вывести список избраных
    def list(self, request, *args, **kwargs):
        favorite = models.FavoriteRecipe.objects.filter(person=request.user.id).all()
        recipes = models.Recipe.objects.filter(favorite_recipe__in=favorite)
        serializer = serializers.ShortShowReciprSerializer(recipes,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CartShopingViewSet(GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)


    # добавить в список покупок
    def retrieve(self, request, *args, **kwargs):
        recipe = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
        cart, status_ = models.CartShopping.objects.get_or_create(
            person=request.user,
            recipe=recipe,
        )
        if status_:
            serializer = serializers.ShortShowReciprSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = {
                'errors' : 'Данный рецепт уже добавлен в список покупок'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


    #Удалить из списка покупок
    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
        try:
            tmp = models.CartShopping.objects.get(
                person=request.user,
                recipe=recipe,
            )
            tmp.delete()
        except:
            error = {
                'errors' : 'Данного рецепта нет в корзине'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)



# Скачать списка покупок
class DownloadCart(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)


    def list(self, request, *args, **kwargs):
        cart = models.CartShopping.objects.filter(person=request.user.id).all()
        recipe = models.Recipe.objects.filter(in_cart__in=cart).all()
        ingredients = models.RecipeIngredient.objects.filter(
            recipe__in=recipe).all()

        response = HttpResponse(content_type = 'txt/plain')
        response.write('------Список покупок от Foodgram------\n\n')
        for ingredient in ingredients:
            name_ingredient = ingredient.ingredient.name
            amount = ingredient.amount
            measurement_unit = ingredient.ingredient.measurement_unit
            response.write(f" {name_ingredient} - {amount} {measurement_unit}\n")

        response["Content-Disposition"] = "attachment; filename=shopping_list.txt"
        return response



  



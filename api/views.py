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



class FavoriteViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)


    # добавить в список изброных
    def retrieve(self, request, *args, **kwargs):
        # TODO проверить коретность работы

        recipe = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
        
        favorite, status_ = models.FavoriteRecipe.objects.get_or_create(
            person=request.user,
            recipes=recipe,
        )
        if status_:
            serializer = serializers.ShortShowReciprSerializer(recipe)
            return serializer.data
        else:
            error = {
                'errors': 'Данный рецеп уже добавлен в избраное'
            }
            return Response(error ,status=status.HTTP_400_BAD_REQUEST)


    #Удалить из списка изброных
    def destroy(self, request, *args, **kwargs):
        # TODO проверить работаспособность
        recipe = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
        try:
            tmp = models.FavoriteRecipe.objects.get(
                person=request.user,
                recipes=recipe,
            )
            tmp.delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


    #Вывести список избраных
    def list(self, request, *args, **kwargs):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!LIST')
        favorite = models.FavoriteRecipe.objects.filter(person=request.user.id).all()
        print(favorite)
        recipes = models.Recipe.objects.filter(favorite_recipe__in=favorite)
        print(recipes)
        serializer = serializers.ShortShowReciprSerializer(recipes,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CartShopingViewSet(GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)


    # добавить в список покупок
    def retrieve(self, request, *args, **kwargs):
        # TODO проверить работоспособность
        recipe = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
        cart, status_ = models.CartShopping.objects.get_or_create(
            person=request.user,
            recipes=recipe,
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
        # TODO проверить работоспособность
        recipe = get_object_or_404(models.Recipe, id=self.kwargs['pk'])
        try:
            tmp = models.CartShopping.objects.get(
                person=request.user,
                recipes=recipe,
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
    #permission_classes = (permissions.IsAuthenticated,)


    def list(self, request, *args, **kwargs):
        # TODO проверить роботоспособность, сдлеать отправку файла
        print('!!!!!!!!!!!!!!!!!!!!list')
        print(request.user)
        cart = models.CartShopping.objects.filter(person=request.user.id).all()
        print(cart)
        recipe = models.Recipe.objects.filter(in_cart__in=cart).all()
        print(recipe)
        ingredients = models.RecipeIngredient.objects.filter(
            recipe__in=recipe
        ).all()
        print(ingredients)
        print(os.getcwd())


        response = HttpResponse(content_type = 'txt/plain')
        #response.content_type = 'txt/plain'
        response.write('------Список покупок от Foodgram------\n\n')
        for ingredient in ingredients:
            print('цикл')
            name_ingredient = ingredient.ingredient.name
            amount = ingredient.amount
            measurement_unit = ingredient.ingredient.measurement_unit
            print(f" {name_ingredient} - {amount} {measurement_unit}")
            response.write(f" {name_ingredient} - {amount} {measurement_unit}\n")

        response["Content-Disposition"] = "attachment; filename=shopping_list.txt"
        #response['Content-Dispostion'] = "attachment; filename='shopping-list.txt'"
        return response



  



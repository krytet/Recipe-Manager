from rest_framework import permissions

from users.models import Subscription
from . import serializers
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .permissions import CustomUserPermission
from api.pagination import StandardResultsSetPagination


User = get_user_model()

# Смена пароля
class ResetPasswordView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserPasswordSerilazer
    permission_classes = (permissions.IsAuthenticated,)


class ShowUserView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.ShowUserSerializer
    permission_classes = (CustomUserPermission,)
    pagination_class =  StandardResultsSetPagination
    lookup_field = 'pk'


    # Регистрация нового пользовтеля
    def create(self, request, *args, **kwargs):
        serializer = serializers.RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    # Получение профеля
    # TODO проверить работоспособость
    def retrieve(self, request, *args, **kwargs):
        # Получение своего профеля
        if self.kwargs['pk'] == 'me':
            serializer = self.get_serializer(request.user)
            #serializer = serializers.ShowUserSerializer(request.user)
            #return Response(serializer.data ,status=status.HTTP_200_OK)
        # Получения профеля пользователя с ID
        else:
            user = get_object_or_404(User, id=self.kwargs['pk'])
            serializer = self.get_serializer(user)
        return Response(serializer.data ,status=status.HTTP_200_OK)


class SubscriptionViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class =  StandardResultsSetPagination


    def get_queryset(self):
        subscriptions = Subscription.objects.filter(respondent=self.request.user).all()
        subscriptions = User.objects.filter(subscribers__in=subscriptions).all()
        return subscriptions


    ## Вывод список подписок
    #def list(self, request, *args, **kwargs):
    #    currect_user = request.user
    #    subscriptions = Subscription.objects.filter(respondent=currect_user).all()
    #    subscriptions = User.objects.filter(subscribers__in=subscriptions).all()
    #    serializer = self.get_serializer(subscriptions, many=True)
    #    return Response(serializer.data)


    # Подписаться на прользователя с ID 
    def retrieve(self, request, *args, **kwargs):
        current_user = request.user
        subscriptions = get_object_or_404(User, id=self.kwargs['pk'])
        if current_user == subscriptions:
            error = {
                "errors" : 'Вы не можете подписаться на самого себя'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        subscription, status_c = Subscription.objects.get_or_create(respondent=current_user,
                                                                  subscriptions=subscriptions)
        if not status_c:
            error = {
                "errors" : 'Вы уже подписаны на данного пользователя'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(subscriptions)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # Отписаться от пользователя с ID
    def destroy(self, request, *args, **kwargs):
        current_user = request.user
        subscriptions = get_object_or_404(User, id=self.kwargs['pk'])
        try:
            subscription = Subscription.objects.get(respondent=current_user,
                                     subscriptions=subscriptions)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



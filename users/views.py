from rest_framework import permissions, viewsets

from users.models import Subscription
from . import serializers
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .permissions import CustomUserPermission


User = get_user_model()


class ResetPasswordView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserPasswordSerilazer




class ShowUserView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.ShowUserSerializer
    permission_classes = (CustomUserPermission,)
    lookup_field = 'pk'


    def create(self, request, *args, **kwargs):
        serializer = serializers.RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(User, email= request.data['email'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def retrieve(self, request, *args, **kwargs):

        if self.kwargs['pk'] == 'me':
            serializer = serializers.ShowUserSerializer(request.user)
            return Response(serializer.data ,status=status.HTTP_200_OK)
        else:
            user = get_object_or_404(User, id=self.kwargs['pk'])

        serializer = self.get_serializer(user)
        return Response(serializer.data)


class SubscriptionViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def list(self, request, *args, **kwargs):
        currect_user = request.user
        subscriptions = Subscription.objects.filter(respondent=currect_user).all()
        subscriptions = User.objects.filter(subscribers__in=subscriptions).all()
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)


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
        return Response(serializer.data)

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



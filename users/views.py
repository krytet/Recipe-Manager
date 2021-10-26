from rest_framework import viewsets
from . import serializers
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class ResetPasswordView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserPasswordSerilazer


# TODO обеденить с ShowUser
class ProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ShowUserSerializer

    #TODO настроить для текокущего пользователя
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ShowUserView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.ShowUserSerializer


    def create(self, request, *args, **kwargs):
        serializer = serializers.RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


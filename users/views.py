from rest_framework import permissions, viewsets
from . import serializers
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

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
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'


    def create(self, request, *args, **kwargs):
        serializer = serializers.RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(User, email= request.data['email'])
        #headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

    def retrieve(self, request, *args, **kwargs):

        if self.kwargs['pk'] == 'me':
            # TODO получение текущего пользователя
            return Response(status=status.HTTP_200_OK)
        else:
            user = get_object_or_404(User, id=self.kwargs['pk'])

        serializer = self.get_serializer(user)
        return Response(serializer.data)


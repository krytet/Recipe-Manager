from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views
from .routers import CustomRouter

router = routers.DefaultRouter()
router.register('', views.ShowUserView, basename='users')


urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('recipes', views.RecipeView, basename='recipe')
router.register('tags', views.TagView, basename='tag')




urlpatterns = [
    path('', include(router.urls)),

    #path('hi/', views.Se)

]
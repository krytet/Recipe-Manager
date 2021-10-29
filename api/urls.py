from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views
from users.routers import CustomRouter

router = routers.DefaultRouter()
router.register('recipes', views.RecipeView, basename='recipe')
router.register('tags', views.TagView, basename='tag')

custom_router = CustomRouter()
custom_router.register('favorite', views.FavoriteViewSet, basename='favorite')
custom_router.register('shopping_cart', views.CartShopingViewSet, basename='shopping_cart')





urlpatterns = [
    path('recipes/download_shopping_cart/', views.DownloadCart.as_view(), name='download_cart'),
    path('recipes/', include(custom_router.urls)),
    path('', include(router.urls)),
    path('auth/token/login/', views.CustomObtainAuthToken.as_view()),
    path('auth/token/logout/', views.CustomDeleteAuthToken.as_view()),


    #path('hi/', views.Se)

]
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views
from .routers import CustomRouter

router = routers.DefaultRouter()
router.register('', views.ShowUserView, basename='users')
#router.register('(?P<pk>[^/.]+)/subscribe', views.SubscriptionViewSet, basename='subscribe')
custom_router = CustomRouter()
custom_router.register('subscribe', views.SubscriptionViewSet, basename='subscribe')



urlpatterns = [
    path('set_password/', views.ResetPasswordView.as_view(), name='ResetPassword'),
    #path('subscriptions/'),
    path('', include(custom_router.urls)),
    path('', include(router.urls)),
    
    

    

    #path('hi/', views.Se)

]
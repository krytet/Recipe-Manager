from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.ShowUserView, basename='users')




urlpatterns = [
    path('', include(router.urls)),
    path('set_password/', views.ResetPasswordView.as_view(), name='ResetPassword'),

    

    #path('hi/', views.Se)

]
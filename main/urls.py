from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('performance/', views.performance, name='performance'),
    path('register-client', views.RegisterClient.as_view(), name='register_client'),
#    path('client/<str:pk>',)
]

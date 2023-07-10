from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('performance/', views.performance, name='performance'),
    path('client/registert', views.RegisterClient.as_view(), name='register_client'),
    path('clients', views.ClientList.as_view(), name='client_list'),
    path('client/<str:pk>', views.ClientDetail.as_view(), name='client_detail'),
    path('suppliers', views.SupplierList.as_view(), name='supplier_list'),
    path('supplier/<str:pk>', views.SupplierDetail.as_view(), name='supplier_detail'),
    path('order/create', views.create_order, name='create_order'),

]

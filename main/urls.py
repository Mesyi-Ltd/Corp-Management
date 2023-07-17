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
    path('staff/position/create', views.create_position, name='create_position'),
    path('staff/register', views.staff_register, name='register'),
    path('staff/list', views.StaffList.as_view(), name='staff_list'),
    path('staff/<str:pk>', views.StaffDetail.as_view(), name='staff_detail'),
]

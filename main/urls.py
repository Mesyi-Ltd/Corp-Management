from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('performance/yearly', views.annual_performance, name='yearly_performance'),
    path('performance/monthly', views.monthly_performance, name='monthly_performance'),
    path('client/registert', views.register_client, name='register_client'),
    path('clients', views.ClientList.as_view(), name='client_list'),
    path('client/<str:pk>', views.ClientDetail.as_view(), name='client_detail'),
    path('suppliers', views.SupplierList.as_view(), name='supplier_list'),
    path('supplier/<str:pk>', views.SupplierDetail.as_view(), name='supplier_detail'),
    path('order/create', views.create_order, name='create_order'),
    path('order/list', views.OrderList.as_view(), name='order_list'),
    path('order/download/<str:pk>', views.order_download, name='order_download'),
    path('order/<str:pk>', views.OrderDetail.as_view(), name='order_detail'),
    path('staff/position/create', views.create_position, name='create_position'),
    path('staff/register', views.staff_register, name='register'),
    path('staff/list', views.StaffList.as_view(), name='staff_list'),
    path('staff/<str:pk>', views.StaffDetail.as_view(), name='staff_detail'),
    path('staff/edit/<str:pk>', views.staff_edit, name='staff_edit'),
    path('item/add', views.AddItem.as_view(), name='item_add'),
    path('item/list', views.ItemList.as_view(), name='item_list'),
    path('item/store', views.store_item, name='store_item'),
    path('item/<str:pk>', views.ItemDetail.as_view(), name='item_detail'),
    path('data/annual', views.get_annual_data, name='annual_data'),
    path('data/month', views.get_month_data, name='month_data')
]

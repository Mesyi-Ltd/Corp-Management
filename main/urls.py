from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),


    path('performance/yearly', views.annual_performance, name='yearly_performance'),
    path('performance/monthly', views.monthly_performance, name='monthly_performance'),


    path('client/register', views.register_client, name='register_client'),
    path('clients', views.ClientList.as_view(), name='client_list'),
    path('client/<str:pk>', views.ClientDetail.as_view(), name='client_detail'),


    path('suppliers', views.SupplierList.as_view(), name='supplier_list'),
    path('supplier/create', views.CreateSupplier.as_view(), name='supplier_create'),
    path('supplier/<str:pk>', views.SupplierDetail.as_view(), name='supplier_detail'),
    path('supplier/<str:pk>/download', views.price_download, name='supplier_download'),


    path('order/create', views.create_order, name='create_order'),
    path('order/list', views.OrderList.as_view(), name='order_list'),
    path('order/download/<str:pk>', views.order_download, name='order_download'),
    path('order/<str:pk>', views.OrderDetail.as_view(), name='order_detail'),
    path('order/<str:pk>/purchase/create', views.add_purchase, name='purchase_add'),
    path('order/<str:pk>/purchase/edit', views.edit_purchase, name='purchase_edit'),
    path('order/<str:pk>/purchase/detail', views.purchase_detail, name='purchase_detail'),
    path('order/<str:pk>/production/create', views.production_create, name='production_add'),
    path('order/<str:pk>/production/list', views.ProductionList.as_view(), name='production_list'),


    path('staff/position/create', views.create_position, name='create_position'),
    path('staff/register', views.staff_register, name='register'),
    path('staff/list', views.StaffList.as_view(), name='staff_list'),
    path('staff/<str:pk>', views.StaffDetail.as_view(), name='staff_detail'),
    path('staff/edit/<str:pk>', views.staff_edit, name='staff_edit'),


    path('item/add', views.AddItem.as_view(), name='item_add'),
    path('item/list', views.ItemList.as_view(), name='item_list'),
    path('item/<str:pk>', views.ItemDetail.as_view(), name='item_detail'),


    path('storage/create', views.storage_change, name='create_change'),
    path('storage/update/<str:pk>', views.update_storage_change, name='storage_change'),
    path('storage/complete/<str:pk>', views.change_complete, name='change_complete'),
    path('storage/change/item/delete/<str:pk>', views.delete_item_change, name='delete_item_change'),
    path('storage/<str:pk>', views.change_detail, name='change_detail'),


    path('production/<str:pk>', views.production_detail, name='production_detail'),

    path('order/<str:pk>/quality/list', views.QualityList.as_view(), name='quality_list'),
    path('order/<str:pk>/quality/create', views.quality_create, name='quality_create'),
    path('quality/<str:pk>', views.quality_detail, name='quality_detail'),
]

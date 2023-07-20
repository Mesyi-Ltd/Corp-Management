from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(Client)
admin.site.register(Staff)
admin.site.register(Company)
admin.site.register(Perm)
admin.site.register(Position)
admin.site.register(MonthlyPerformance)
admin.site.register(ClientContact)
admin.site.register(ClientCommunication)
admin.site.register(Supplier)
admin.site.register(SupplierContact)
admin.site.register(OrderStatus)
admin.site.register(OrderAttachment)
admin.site.register(Item)

# Register your models here.

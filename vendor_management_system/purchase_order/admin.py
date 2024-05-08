from django.contrib import admin
from purchase_order.models import PurchaseOrder
from purchase_order.models import HistoricalPerformance

admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)
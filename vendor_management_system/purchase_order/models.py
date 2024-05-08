from datetime import datetime
from django.db.models import JSONField
from django.db import models
from vendor.models import VendorModel


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=255,primary_key=True, unique=True)
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now=True)
    acknowledgment_date = models.DateTimeField(null=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def acknowledge(self):
        self.acknowledgment_date = datetime.now()
        self.save()
        self.vendor.calculate_average_response_time()

    def complete(self, quality_rating):
        self.status = 'completed'
        self.quality_rating = quality_rating
        self.save()
        self.vendor.calculate_on_time_delivery_rate()
        self.vendor.calculate_quality_rating_avg()
        self.vendor.calculate_fulfillment_rate()
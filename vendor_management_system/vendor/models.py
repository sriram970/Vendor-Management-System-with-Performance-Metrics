from datetime import datetime

from django.db import models

class VendorModel(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=25,primary_key=True,unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def calculate_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        on_time_orders = completed_orders.filter(delivery_date__lte=datetime.now())
        if completed_orders.count() > 0:
            self.on_time_delivery_rate = (on_time_orders.count() / completed_orders.count()) * 100
        else:
            self.on_time_delivery_rate = 0
        self.save()

    def calculate_quality_rating_avg(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        if completed_orders.count() > 0:
            self.quality_rating_avg = completed_orders.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
        else:
            self.quality_rating_avg = 0
        self.save()

    def calculate_average_response_time(self):
        acknowledged_orders = self.purchaseorder_set.exclude(acknowledgment_date=None)
        if acknowledged_orders.count() > 0:
            total_response_time = sum([(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_orders])
            self.average_response_time = total_response_time / acknowledged_orders.count()
        else:
            self.average_response_time = 0
        self.save()

    def calculate_fulfillment_rate(self):
        total_orders = self.purchaseorder_set.count()
        fulfilled_orders = self.purchaseorder_set.filter(status='completed').count()
        if total_orders > 0:
            self.fulfillment_rate = (fulfilled_orders / total_orders) * 100
        else:
            self.fulfillment_rate = 0
        self.save()
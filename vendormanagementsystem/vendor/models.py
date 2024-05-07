from django.db import models

class VendorModel(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(primary_key=True,unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)






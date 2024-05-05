from django.db import models

# Create your models here.


class Vendors(models.Model):
    name=models.CharField(max_length=30) #CharField - Vendor's name.
    contact_details=models.TextField() #: TextField - Contact information of the vendor
    address=models.TextField() #TextField - Physical address of the vendor.
    vendor_code=models.CharField(max_length=15,unique=True) #CharField - A unique identifier for the vendor
    on_time_delivery_rate=models.FloatField(default=0.0) #: FloatField - Tracks the percentage of on-time deliveries
    quality_rating_avg=models.FloatField(default=0.0) #FloatField - Average rating of quality based on purchase orders
    average_response_time=models.FloatField(default=0.0) #FloatField - Average time taken to acknowledge purchase orders
    fulfillment_rate=models.FloatField(default=0.0) #: FloatField - Percentage of purchase orders fulfilled successfully

class PurchaseOrder(models.Model):
    po_number=models.CharField(max_length=20,unique=True) #: CharField - Unique number identifying the PO.
    vendor=models.ForeignKey(Vendors,on_delete=models.CASCADE) #: ForeignKey - Link to the Vendor model.
    order_date=models.DateTimeField(auto_now_add=True) #: DateTimeField - Date when the order was placed
    delivery_date=models.DateTimeField(null=True) #: DateTimeField - Expected or actual delivery date of the order
    items=models.JSONField() #JSONField - Details of items ordered.
    quantity=models.IntegerField() #IntegerField - Total quantity of items in the PO.
    status=models.CharField(max_length=10) #CharField - Current status of the PO (e.g., pending, completed, canceled
    quality_rating=models.FloatField(null=True) #: FloatField - Rating given to the vendor for this PO (nullable).
    issue_date=models.DateField(null=True) #DateTimeField - Timestamp when the PO was issued to the vendor
    acknowledgment_date=models.DateTimeField(null=True) #DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.


class HistoricalPerformance(models.Model):
    vendor=models.ForeignKey(Vendors,on_delete=models.CASCADE)     #ForeignKey - Link to the Vendor model.
    date=models.DateTimeField(null=True) #DateTimeField - Date of the performance record.
    on_time_delivery_rate=models.FloatField() #FloatField - Historical record of the on-time delivery rate.
    quality_rating_avg=models.FloatField() #FloatField - Historical record of the quality rating average.
    average_response_time=models.FloatField()  #FloatField - Historical record of the average response time.
    fulfillment_rate=models.FloatField() #FloatField - Historical record of the fulfilment rat
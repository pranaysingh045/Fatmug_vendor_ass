from rest_framework.decorators import APIView
from rest_framework import status,serializers
from vendorapp.models import *
# from rest_framework.serializers import Serializer


class VendorCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model=Vendors
        fields=['name','address','contact_details','vendor_code']

    def create(self, validated_data):
        print('this is vendor create',validated_data)
        return super().create(validated_data)

class VendorListSerializers(serializers.ModelSerializer):
    class Meta:
        model=Vendors
        fields='__all__'

class PurchaseOrderCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields=['po_number','vendor','delivery_date','items','quantity','status']

class orderListSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=PurchaseOrder
        fields='__all__'

class UpdatePurchaseOrderSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=PurchaseOrder
        fields=['items','quantity','status','quality_rating','issue_date','acknowledgment_date']

class UpdateAcknowledgeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=PurchaseOrder
        fields=['acknowledgment_date']

        
class HistoricalPerformanceSerializers(serializers.ModelSerializer):
    class Meta:
        model=HistoricalPerformance
        fields='__all__'
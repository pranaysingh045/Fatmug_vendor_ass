from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import APIView,api_view,permission_classes,authentication_classes
from rest_framework import status
from vendorapp.serializers import *
import uuid
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from vendorapp.models import PurchaseOrder
from django.shortcuts import get_object_or_404
from django.db.models import Count ,Avg,ExpressionWrapper,DurationField,F
# Create your views here.

def home(request):
    print('this is home')
    return HttpResponse('this is home and test')
@api_view(['POST'])
def GenerateToken(request):
    vendorId=request.data.get('vendorId') #use can use id also it vendor_code is also unique so can use
    password=request.data.get('password')
    
    try:
        if vendorId and password:
            vendorobj=Vendors.objects.get(id=vendorId)
            user=User.objects.create_user(username=(vendorobj.name+vendorobj.vendor_code),password=password)
            userToken,created=Token.objects.get_or_create(user=user)
            return Response({'msg':'User created successfully','api_token':str(userToken)},status=status.HTTP_200_OK)
        else:
            return Response({'msg':'all field required'},status=status.HTTP_400_BAD_REQUEST)
    except Vendors.DoesNotExist:
        return Response({'msg':'vendor not found'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print('this is token err',e)
        return Response({'msg':'Internal server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# def generateUniqCode():
#     timestamp=uuid.uuid4()
#     return 
class CreatVendor(APIView):
    def post(self,request):
        try:
            vendor_code=str(uuid.uuid4())[:8]
            vendorname=request.data.get('name')
            print('this is name v',vendorname)
            data=request.data
            data['vendor_code']=vendor_code
            
            serializerdata=VendorCreateSerializers(data=data)
            if serializerdata.is_valid():
                serializerdata.save()
                return Response({'msg':'vendor created'},status=status.HTTP_201_CREATED)
            else:
                return Response(serializerdata.error_messages,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('this is create vendor error',e)
            return Response({'msg':'Interserver error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self,request,vendor_id=None):

        try:
            if vendor_id:
                vendorlist=Vendors.objects.get(id=vendor_id)
                serializers=VendorListSerializers(vendorlist)
            else:
                vendorlist=Vendors.objects.all()
                serializers=VendorListSerializers(vendorlist,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'msg':'Something is wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request,vendor_id=None):

        try:
            if vendor_id:
                vendordetails=Vendors.objects.get(id=vendor_id)
                serializedata=VendorListSerializers(vendordetails,request.data)
                if serializedata.is_valid():
                    serializedata.save()
                    return Response(serializedata.data,status=status.HTTP_200_OK)
                else:
                    return Response({'msg':'details updated'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg':'Vendor Id is missing'},status=status.HTTP_400_BAD_REQUEST)
        
        except Vendors.DoesNotExist:
            return Response({'msg':'vendor not found'},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'msg':'Internal server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self,request,vendor_id):
        try:
            if vendor_id:
                vendordetails=Vendors.objects.get(id=vendor_id)
                vendordetails.delete()
                return Response({'msg':'deleted successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Vendor Id is missing'},status=status.HTTP_400_BAD_REQUEST)
        except Vendors.DoesNotExist:
            return Response({'msg':'Vendor not found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'msg':'Internal server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
        
        
        
            
        
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])    
class PurchaseOrders(APIView):
    def post(self,request):
        us=request.user
        # print('this is request',request.data)
        # print('this is us',us,'data',datetime.now())
         #order details(e PO number, vendor reference,order date, items, quantity, and status.)
        try:
            user_refId=str(us)[-8:]
            print('this is re',user_refId)
            vendodetails=Vendors.objects.get(vendor_code=user_refId)
            po_number=str(uuid.uuid4())[:20]
            vendor=vendodetails.id
            data=request.data
            # delivery_date_str = '2024-15-04 12:52:09.931380'
            delivery_date_obj = datetime.strptime(request.data.get('delivery_date'), '%Y-%m-%d %H:%M:%S.%f')
            data['delivery_date']=delivery_date_obj
            data['po_number']=po_number
            data['vendor']=vendor
            print('this is data before re',data)
            serializedata=PurchaseOrderCreateSerializers(data=data)
            if serializedata.is_valid():
                serializedata.save()
                return Response({'msg':'order successfully'},status=status.HTTP_201_CREATED)
            else:
                return Response(serializedata.error_messages,status=status.HTTP_400_BAD_REQUEST)
        except Vendors.DoesNotExist:
            return Response({'msg':'Not found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('this is create order error',e)
            return Response({'msg':'Internal server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self,request,po_id=None):
        requestuser=request.user
        user_refId=str(requestuser)[-8:]
        try:
            if user_refId:
               vendordetails=get_object_or_404(Vendors,vendor_code=user_refId)
               if(po_id):
                   orderdetails=PurchaseOrder.objects.get(vendor=vendordetails,id=po_id)
                   print('this is order deta',orderdetails)
                   serializedata=orderListSerializers(orderdetails)
               else:
                    orderdetails=PurchaseOrder.objects.filter(vendor=vendordetails)
                    print('this is order deta',orderdetails)
                    serializedata=orderListSerializers(orderdetails,many=True)
               return Response(serializedata.data,status=status.HTTP_200_OK)
            else:
                return Response({'msg':'refrence not found'},status=status.HTTP_400_BAD_REQUEST)
        except Vendors.DoesNotExist:
            return Response({'msg':'User not found'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('this is error',e)
            return Response({'msg':'Internal server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self,request,po_id):
        req_user=request.user
        refId=str(req_user)[-8:]
        try:
            vendordetails=get_object_or_404(Vendors,vendor_code=refId)
            orderdetails=PurchaseOrder.objects.get(vendor=vendordetails,id=po_id)
            data=request.data
            print('this is update data',data)
            print('this is update data',orderdetails)
            # data['vendor']=vendordetails.id
            serializersdata=UpdatePurchaseOrderSerializers(orderdetails,data=data)
            if serializersdata.is_valid():
                serializersdata.save()
                print(serializersdata.data)
                return Response(serializersdata.data,status=status.HTTP_200_OK)
            else:
                return Response(serializersdata.error_messages,status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({'msg':'order not found'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print('this is err',e)
            return Response({'msg':'Intername error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,po_id):
        re_user=request.user
        ref_id=str(re_user)[-8:]
        try:
            if(ref_id):
                orderdetails=PurchaseOrder.objects.get(id=po_id,vendor__vendor_code=ref_id)
                orderdetails.delete()
                print('thi delete',orderdetails)
                return Response({'msg':'Delete successfully'},status=status.HTTP_200_OK)
            
        except PurchaseOrder.DoesNotExist:
             return Response({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({'msg':'internal error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
    

class VendorPerFormance(APIView):
    def post(self,request,vendor_id):
        print('this is performace vendor id',vendor_id)
        try:
            # vendor=get_object_or_404(Vendors,id=vendor_id)
            vendor=Vendors.objects.get(id=vendor_id)
            total_completeOrder=PurchaseOrder.objects.filter(vendor=vendor,status='complite')
            totalCompleteOrder=total_completeOrder.count()
            print('this is completer order',total_completeOrder.count())
            noofOntimedelivery_order=total_completeOrder.filter(acknowledgment_date__lte=models.F('delivery_date')).count()
            print('ontime delivery date',noofOntimedelivery_order)
            ontimedeliverrate=(noofOntimedelivery_order/totalCompleteOrder)*100 if totalCompleteOrder!=0 else 0
            vendor.on_time_delivery_rate=ontimedeliverrate
        

            #Quality rating
            qualityrating=total_completeOrder.exclude(quality_rating__isnull=True)
            averagerating=qualityrating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
            vendor.quality_rating_avg=averagerating
            print('quality avg count',averagerating)
            #vendor.quality_rating_avg=averagerating

            # Fulfillment Rate
            totlvendororder=PurchaseOrder.objects.filter(vendor=vendor).count()
            fulfillment_rate=(total_completeOrder.count()/totlvendororder)*100 if totlvendororder!=0 else 0
            print('this is fulfilment rate',fulfillment_rate)
            vendor.fulfillment_rate=fulfillment_rate

            #Average Response Time:
            totalacknowledgeItem=total_completeOrder.exclude(acknowledgment_date__isnull=True)
            print('total acknolodge item',totalacknowledgeItem)
          
            responsetime=totalacknowledgeItem.annotate(response_time=Avg(models.F('acknowledgment_date') - models.F('issue_date'))).aggregate(Avg('response_time'))['response_time__avg'] or 0
            print('this is response time',responsetime)
            vendor.average_response_time=responsetime
            vendor.save()
            #hist_vend_perfor=HistoricalPerformance.objects.update_or_create(vendor=vendor,date=datetime.now(),on_time_delivery_rate=ontimedeliverrate,quality_rating_avg=averagerating,average_response_time=responsetime,fulfillment_rate=fulfillment_rate)
            HistoricalPerformance.objects.update_or_create(
                vendor=vendor,
                date=timezone.now(),
                defaults={
                    'on_time_delivery_rate': ontimedeliverrate,
                    'quality_rating_avg': averagerating,
                    'average_response_time': responsetime,
                    'fulfillment_rate': fulfillment_rate
                }
            )
            
            return Response({'msg':'Performance update successfull'},status=status.HTTP_200_OK)
            
            
        except Vendors.DoesNotExist:
            return Response({'msg':'Vendor not found'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('error orp',e)
            return Response({'msg':'some thing wrong'},status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self,request,vendor_id):
        try:
            vendor=Vendors.objects.get(id=vendor_id)
            historicalvendor=HistoricalPerformance.objects.filter(vendor=vendor)
            serializersdata=HistoricalPerformanceSerializers(historicalvendor,many=True)
            return Response(serializersdata.data,status=status.HTTP_200_OK)
        except Vendors.DoesNotExist:
            return Response({'msg':'Vendor not found'},status=status.HTTP_404_NOT_FOUND)
  
        except Exception as e:
            print('thus is s',e)
            return Response({'msg':'something wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

       
    

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])   
class updateAcklodgement(APIView):
    def post(self,request,po_id):
        try:
            orderdetails=PurchaseOrder.objects.get(id=po_id)
            ack=request.data.get('acknowledgment_date')
            print('this sck',request.data)
            serializerdata=UpdateAcknowledgeSerializers(orderdetails,data=request.data)
            if serializerdata.is_valid():
                serializerdata.save()
                return Response({'msg':'update successfully'},status=status.HTTP_200_OK)
            return Response(serializerdata.error_messages,status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(e)
            return Response({'msg':'something wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




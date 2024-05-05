from django.urls import include,path
from vendorapp import views
urlpatterns=[
    path('home/',views.home,name='test'),
    path('api/vendors/',views.CreatVendor.as_view(),name='create vendor'),
    path('api/vendors/<int:vendor_id>',views.CreatVendor.as_view(),name='create vendor'),
    path('api/generatetoken',views.GenerateToken,name='generate user token'),
    path('api/purchase_orders/',views.PurchaseOrders.as_view(),name='createorder'),
    path('api/purchase_orders/<int:po_id>/',views.PurchaseOrders.as_view(),name='getsingleproduct'),
    path('api/purchase_orders/<int:po_id>/acknowledge',views.updateAcklodgement.as_view(),name='update acknowledge of PO'),
    path('api/vendors/<int:vendor_id>/performance',views.VendorPerFormance.as_view(),name='update performance'),
    #path('api/purchase_orders/<int:po_id>/acknowledge',views.VendorHistoricalPerformance.as_view(),name='get performance')

]
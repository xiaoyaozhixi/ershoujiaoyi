from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    path('place_order_more/', views.place_order_more),
    path('place_order/', views.place_order),
    path('AlipayView/', views.AlipayView),
    path('payresult/', views.payresult)
]
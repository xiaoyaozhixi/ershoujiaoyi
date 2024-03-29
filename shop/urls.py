from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
app_name = 'shop'
urlpatterns = [
    path('main/', views.main, name='main'),
    path('book_list/', views.book_list),
    path('digital_list/', views.digital_list),
    path('cloth_list/', views.cloth_list),
    path('game_list/', views.game_list),
    path('other_list', views.other_list),
    path('daily_list/', views.daily_list),
    path('release/', views.release),
    path('release_goods/', views.release_goods),
    path('rewrite_goods/<int:pk>/', views.rewrite_goods),
    path('delete_goods/<int:pk>/', views.delete_goods),
    path('add_to_cart/<int:pk>/', views.add_to_cart),
    path('search_result/', views.search_result),
    path('clt_goods/<int:pk>/', views.clt_goods, name='clt_goods'),
    path('details/<int:pk>/', views.details, name='details'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_URL)

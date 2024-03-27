from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

app_name = 'user'
urlpatterns = [
    path('', views.login),
    path('login_handle/', views.login_handle),
    path('logout/', views.logout),
    path('register/', views.register, name='register'),
    path('register_handle/', views.register_handle),
    path('user_center/', views.user_center, name='user_center'),
    path('reset_password/', views.reset_password),
    path('reset_password_handle/', views.reset_password_handle),
    path('user_center/', views.user_center),
    path('user_change/', views.user_change),
    path('user_change_handle/', views.user_change_handle),
    path('my_cart/', views.my_cart),
    path('cart/', views.cart, name='cart'),
    path('delete_cart', views.delete_cart),
    path('collection/', views.collection, name='collection'),
    path('remove_clt_goods/<int:pk>/', views.remove_clt_goods),
    path('change_password/', views.change_password),
    path('my_post/', views.my_post),
    path('my_order/', views.my_order),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_URL)

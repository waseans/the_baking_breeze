# thebakingbreeze/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about_us/', views.about_us, name='about_us'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
        path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.user_orders, name='user_orders'),
     path('order/<int:order_id>/', views.order_details_full, name='order_details_full'),
     path('verify-payment/', views.verify_payment, name='verify_payment'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

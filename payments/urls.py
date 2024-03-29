from django.urls import path
from . import views
from . import webhooks

app_name = 'payments'


urlpatterns = [
    path('process/', views.order_create, name='process'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('add/to/cart/<int:course_id>/', views.add_to_cart, name='add_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove/from/cart/<int:course_id>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.clear_cart, name='cart_clear'),

    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]
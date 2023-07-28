from django.urls import path
from orderapp import views

urlpatterns = [
    path("payment/", views.PaymentView.as_view(), name="payment"),
    path("basket/", views.BasketView.as_view(), name="basket"),
    path("orders/", views.OrderView.as_view(), name="orders"),
    path("orders/<int:id>/", views.OrderDetailView.as_view(), name="detail_orders"),
]

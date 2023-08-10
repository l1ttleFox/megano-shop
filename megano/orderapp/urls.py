from django.urls import path
from orderapp import views

app_name = "orderapp"

urlpatterns = [
    path("payment/<int:pk>", views.PaymentView.as_view(), name="payment"),
    path("basket/", views.BasketView.as_view(), name="basket"),
    path("basket", views.BasketView.as_view(), name="basket_redirect"),
    path("order/<int:id>", views.OrderDetailView.as_view(), name="detail_orders"),
    path("orders", views.OrderView.as_view(), name="orders"),
]

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from orderapp.models import Order, Payment, OrderProduct
from orderapp.basket import BasketManager
from orderapp.serializers import OrderSerializer, ShortOrderSerializer


class PaymentView(APIView):
    """View оплаты заказа."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        data = json.loads(json.dumps(request.data))

        order = get_object_or_404(Order, id=int(pk))
        print(order.status)
        if order.status == "posted":
            payment = Payment.objects.create(**data, order=order)
            payment.save()

            for i_order_product in order.basket.order_products.all():
                if i_order_product.count > i_order_product.product.count:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                i_order_product.product.count -= i_order_product.count
                i_order_product.delete()

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BasketView(APIView):
    """View корзины покупок."""

    def get(self, request):
        manager = BasketManager(request)
        return Response(manager.basket_data())

    def post(self, request):
        manager = BasketManager(request)
        data = json.loads(json.dumps(request.data))
        product_id = data.get("id")
        product_count = data.get("count")
        manager.add(int(product_id), int(product_count))

        return Response(manager.basket_data())

    def delete(self, request):
        manager = BasketManager(request)
        data = json.loads(json.dumps(request.data))
        product_id = data.get("id")
        product_count = data.get("count")
        manager.delete(int(product_id), int(product_count))

        return Response(manager.basket_data())


class OrderView(APIView):
    """View заказов."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        selected_orders = Order.objects.filter(
            user__username=request.user.username, status="accepted"
        ).all()
        serialized_data = OrderSerializer(selected_orders, many=True).data

        return Response(serialized_data)

    def post(self, request):
        basket_manager = BasketManager(request)
        data = json.loads(json.dumps(request.data))
        new_order = basket_manager.post_order(request, data)
        serialized_data = ShortOrderSerializer(new_order).data

        return Response(serialized_data)


class OrderDetailView(APIView):
    """Детальный view заказа."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        selected_order = Order.objects.get(id=int(id))
        serialized_data = OrderSerializer(selected_order).data

        return Response(serialized_data)

    def post(self, request, id):
        serialized_data = json.loads(json.dumps(request.data))
        order = Order.objects.get(id=id)
        order.user = User.objects.get(username=request.user.username)
        order.deliveryType = serialized_data.get("deliveryType")
        order.paymentType = serialized_data.get("paymentType")
        order.status = serialized_data.get("status")
        order.city = serialized_data.get("city")
        order.address = serialized_data.get("address")
        order.save()

        products_id_count = dict()
        for i_product in serialized_data.get("products"):
            products_id_count[str(i_product.get("id"))] = int(i_product.get("count"))

        for i_product in order.basket.order_products.all():
            if str(i_product.id) in products_id_count.keys():
                if not int(i_product.count) == products_id_count.get(i_product.id):
                    i_product.count = products_id_count.get(i_product.id)

            elif OrderProduct.objects.get(id=i_product.id):
                product = OrderProduct.objects.get(id=i_product.id)
                product.count = products_id_count.get(product.id)
                order.basket.order_products.add(product)
                order.save()

            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_data = ShortOrderSerializer(order).data

        return Response(serialized_data)

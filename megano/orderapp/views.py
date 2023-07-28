from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from orderapp.models import Order, Payment
from orderapp.basket import BasketManager
from orderapp.serializers import OrderSerializer


class PaymentView(APIView):
    """ View оплаты заказа. """
    
    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        order_id = json.loads(serialized_data).get("id")
        data = json.loads(request.body)
        
        try:
            payment = Payment.objects.create(**data)
            payment.order = Order.objects.get(id=int(order_id))
            payment.save()
            return Response(status=status.HTTP_200_OK)
        
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class BasketView(APIView):
    """ View корзины покупок. """
    
    def get(self, request):
        manager = BasketManager(request)
        return manager.basket_data()
    
    def post(self, request):
        manager = BasketManager(request)
        data = json.loads(request.body)
        product_id = data.get("id")
        product_count = data.get("count")
        manager.set_product_amount(int(product_id), int(product_count))
        return manager.basket_data()
        
    def delete(self, request):
        return self.post(request)
    

class OrderView(APIView):
    """ View заказов. """
    
    def get(self, request):
        return Response(OrderSerializer(Order.objects.all(), many=True).data)
    
    def post(self, request):
        pass


class OrderDetailView(APIView):
    """ Детальный view заказа. """
    
    def get(self, request):
        serialized_data = list(request.POST.keys())[0]
        order_id = json.loads(serialized_data).get("id")
        selected_order = Order.objects.get(id=int(order_id))
        return Response(OrderSerializer(selected_order).data)
    
    def post(self, request):
        pass

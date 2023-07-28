from megano.settings import BASKET_SESSION_ID
from orderapp.models import Basket, OrderProduct
from productapp.models import Product
from orderapp.serializers import OrderSerializer


class BasketManager:
    """Менеджер для управления корзиной покупок."""

    def __init__(self, request):
        """Метод для привязки сессии к экземпляру класса менеджера."""

        self.session = request.session
        basket = self.session.get(BASKET_SESSION_ID)

        if not basket:
            basket = Basket.objects.create()
            self.session[BASKET_SESSION_ID] = basket
        self.basket = basket

    def set_product_amount(self, product_id: int, product_count: int):
        """Метод для изменения кол-ва товара в корзине."""

        if product_id in [
            i_order_product.product.id for i_order_product in self.basket.order_products
        ]:
            for i_order_product in self.basket.order_products:
                if product_id == i_order_product.product.id:
                    i_order_product.count = product_count

        else:
            selected_product = Product.objects.filter(id=product_id).first()
            new_order_product = OrderProduct.objects.create(count=product_count)
            new_order_product.product.add(selected_product)
            new_order_product.basket.add(self.basket)
            new_order_product.save()

        self.save()

    def save(self):
        """Метод для сохранения корзины в сессию."""

        self.session[BASKET_SESSION_ID] = self.basket
        self.session.modified = True

    def clear(self):
        """Метод для удаления корзины из сессии."""

        del self.session[BASKET_SESSION_ID]
        self.session.modified = True

    def basket_data(self):
        data = OrderSerializer(self.basket.order_products, many=True).data
        return data

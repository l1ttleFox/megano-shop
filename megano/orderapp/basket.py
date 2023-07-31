from django.contrib.auth.models import User
from megano.settings import BASKET_SESSION_ID
from orderapp.models import Basket, OrderProduct, Order
from productapp.models import Product
from orderapp.serializers import OrderSerializer
from productapp.serializers import ProductShortSerializer


class BasketManager:
    """Менеджер для управления корзиной покупок."""

    def __init__(self, request):
        """Метод для привязки сессии к экземпляру класса менеджера."""

        self.session = request.session
        self.basket = None

    def get_basket(self):
        basket = None
        basket_id = self.session.get(BASKET_SESSION_ID)
        if basket_id:
            basket = Basket.objects.get(id=int(basket_id))
        if not basket:
            basket = Basket.objects.create()
            self.session[BASKET_SESSION_ID] = basket.id

        return basket

    def set_product_amount(self, product_id: int, product_count: int):
        """Метод для изменения кол-ва товара в корзине."""

        self.basket = self.get_basket()

        if product_id in [
            i_order_product.product.id for i_order_product in self.basket.order_products
        ]:
            for i_order_product in self.basket.order_products:
                if product_id == i_order_product.product.id:
                    i_order_product.count = product_count

        else:
            selected_product = Product.objects.get(id=product_id)
            new_order_product = OrderProduct.objects.create(count=product_count)
            new_order_product.product = selected_product
            new_order_product.basket = self.basket
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
        """Метод получения сериализованных данных корзины."""

        self.basket = self.get_basket()

        data = ProductShortSerializer(self.basket.order_products.all(), many=True).data
        print(type(data))
        return 1

    def post_order(self, request, products_data: dict):
        """Метод публикации нового заказа."""

        self.basket = self.get_basket()

        user = User.objects.get(username=request.user.username)
        products_id_count = dict()
        for i_product in products_data:
            products_id_count[str(i_product.get("id"))] = int(i_product.get("count"))

        use_current_basket = True
        for i_product in self.basket.order_products:
            if not (
                str(i_product.id) in products_id_count.keys()
                and i_product.price == products_data[i_product.id]
            ):
                use_current_basket = False
        if not use_current_basket:
            for i_product_id in products_id_count.keys():
                i_product = OrderProduct.objects.get(id=int(i_product_id))
                i_product.count = products_id_count[i_product_id]
                self.basket.order_products.add(i_product)

        new_order = Order.objects.create(user=user, basket=self.basket)
        self.save()

        return new_order

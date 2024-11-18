from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from store.models import Product, Collection, Review, CartItem, Cart, Order, OrderItem
from user.models import Customer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'inventory', 'price_with_discount', 'collection']

    collection = serializers.StringRelatedField()
    price_with_discount = serializers.SerializerMethodField(method_name='discount_price')

    # title = serializers.CharField(max_length=200)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # inventory = serializers.IntegerField()

    def discount_price(self, product: Product):
        return product.price * Decimal(0.10)


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'inventory', 'collection']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'customer', 'product', 'title', 'content']


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title", "description", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total = serializers.SerializerMethodField(
        method_name='get_total_price'
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.price * cart_item.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total = serializers.SerializerMethodField(
        method_name='get_total_price'
    )

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']


class CreateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = []


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            return self.instance

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']


class UpdateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    class meta:
        model = OrderItem
        fields = ['id', '', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'order_items']


class CreateOrderSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['card_id']
            user_id = self.context['user_id']

            customer = get_object_or_404(Customer, id=user_id)
            cart_item = Cart.objects.filter(cart_id=cart_id)
            order = Order.objects.create(customer=customer)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.price
                ) for item in cart_item
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()

        # customer = get_object_or_404(Customer, id=user_id)
        # cart_item = CartItem.objects.filter(cart_id=cart_id)
        # order = Order.objects.create(customer=customer)
        #
        # cartItem.objects.create(cart_id=cart_id)

# class Meta:
#     model = CartItem
#     fields = ['cart', 'quantity', 'product']


# class OrderSerializer(serializers.ModelSerializer):
#     cart_id = serializers.IntegerField()
#     ord

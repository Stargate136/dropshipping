from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from store.models import *


User = get_user_model()

class ProductTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Product Test",
            price=10,
            description="This is a test product")

    def test_product_slug_is_automatically_generated(self):
        self.assertEqual(self.product.slug, "product-test")

    def test_product_absolute_url_reverse(self):
        self.assertEqual(self.product.get_absolute_url(),
                         reverse("store:product-detail", kwargs={"slug": self.product.slug}))

    def test_product_absolute_url_str(self):
        self.assertEqual(self.product.get_absolute_url(),
                         f"/product/product-test/")


class CartTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email="test@gmail.com",
            password="123456"
        )
        product = Product.objects.create(name="Product Test")
        self.cart = Cart.objects.create(user=user)
        order = Order.objects.create(user=user, product=product)
        self.cart.orders.add(order)
        self.cart.save()

    def test_orders_changed_when_cart_is_ordered(self):
        orders_pk = [order.pk for order in self.cart.orders.all()]
        self.cart.ordered()
        for order_pk in orders_pk:
            order = Order.objects.get(pk=order_pk)
            self.assertIsNotNone(order.ordered_date)
            self.assertTrue(order.ordered)

    def test_orders_deleted_when_cart_is_deleted(self):
        orders_pk = [order.pk for order in self.cart.orders.all()]
        self.cart.delete()
        for order_pk in orders_pk:
            with self.assertRaises(Order.DoesNotExist):
                order = Order.objects.get(pk=order_pk)

    def test_add_product(self):
        product = Product.objects.create(name="Product Test add product")
        self.cart.add_product(slug="product-test-add-product")
        self.assertEqual(self.cart.orders.count(), 2)
        self.assertEqual(self.cart.orders.all()[1].product.slug, "product-test-add-product")

        self.cart.add_product(slug="product-test-add-product")
        self.assertEqual(self.cart.orders.all()[1].quantity, 2)
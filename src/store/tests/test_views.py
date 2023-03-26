from django.test import TestCase
from django.urls import reverse

from store.models import *


class StoreTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Category Test", description="This is a test category")
        self.product = Product.objects.create(
            name="Product Test",
            price=10,
            description="This is a test product",
            category=category)

    def test_products_are_shown_on_store_page(self):
        resp = self.client.get(reverse("store:products-list"))

        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.product.name, str(resp.content))

    def test_connexion_link_shown_when_user_not_connected(self):
        resp = self.client.get(reverse("store:index"))
        self.assertIn("Se connecter", str(resp.content))

    def test_redirect_when_anonymous_user_acces_cart_view(self):
        resp = self.client.get(reverse("store:cart"))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f"{reverse('accounts:login')}?next={reverse('store:cart')}")

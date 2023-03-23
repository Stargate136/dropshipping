from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from iso3166 import countries
import stripe

from shop import settings

stripe.api_key = settings.STRIPE_API_KEY

class ShopperManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("L'adresse email est obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True
        kwargs["is_active"] = True

        return self.create_user(email=email, password=password, **kwargs)


class Shopper(AbstractUser):
    username = None
    email = models.EmailField(max_length=240, unique=True)

    stripe_id = models.CharField(max_length=90, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = ShopperManager()

    def complete_order(self, customer_id):
        self.stripe_id = customer_id
        self.cart.ordered()
        self.save()

    def save_shipping_address(self, address, name):
        ShippingAddress.objects.get_or_create(user=self,
                                              name=name,
                                              city=address["city"],
                                              country=address["country"].lower(),
                                              address_1=address["line1"],
                                              address_2=address["line2"] or "",
                                              zip_code=address["postal_code"])


class ShippingAddress(models.Model):
    user: Shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=240, verbose_name="Nom")

    address_1 = models.CharField(max_length=1024,
                                 help_text="Addresse de voirie et numéro de rue.",
                                 verbose_name="Adresse ligne 1")
    address_2 = models.CharField(max_length=1024,
                                 help_text="Batiment, étage, lieu-dit...",
                                 blank=True,
                                 verbose_name="Adresse ligne 2")
    city = models.CharField(max_length=1024, verbose_name="ville")
    zip_code = models.CharField(max_length=32, verbose_name="Code postal")
    country = models.CharField(max_length=5,
                               choices=[(c.alpha2.lower(), c.name)
                                        for c in countries],
                               verbose_name="Pays")

    alias = models.CharField(max_length=240, blank=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} -> {self.alias}"

    def as_dict(self):
        return {"city": self.city,
                "country": self.country,
                "line1": self.address_1,
                "line2": self.address_2,
                "postal_code": self.zip_code}

    def set_default(self):
        if not self.user.stripe_id:
            raise ValueError(f"{self.user} doesn't have a stripe Customer ID")

        self.user.addresses.update(default=False)
        self.default = True
        self.save()

        stripe.Customer.modify(self.user.stripe_id,
                               address=self.as_dict(),
                               shipping={"name": self.name,
                                         "address": self.as_dict()})


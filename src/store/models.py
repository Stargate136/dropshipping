from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name="nom")
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else static("img/default.jpg")


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name="products")
    name = models.CharField(max_length=128, verbose_name="nom")
    slug = models.SlugField(max_length=128, blank=True)
    price = models.FloatField(default=0.0, verbose_name="prix")
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True,
                                  null=True, verbose_name="image")

    stripe_id = models.CharField(max_length=90, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        self.category = self.category or Category.objects.get_or_create(name="Autre")
        super().save()

    def thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else static("img/default.jpg")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="produit")
    quantity = models.IntegerField(default=1, verbose_name="quantité")
    ordered = models.BooleanField(default=False, verbose_name="commandé")
    ordered_date = models.DateTimeField(blank=True, null=True, verbose_name="Date de commande")

    def __str__(self):
        return f"{self.user.email} -> {self.product} ({self.quantity})"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.email

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.delete()
        super().delete(*args, **kwargs)

    def ordered(self):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        super().delete()

    def add_product(self, slug, quantity):
        product = get_object_or_404(Product, slug=slug)
        order, created = Order.objects.get_or_create(user=self.user,
                                                     product=product,
                                                     ordered=False)
        if created:
            order.quantity = quantity
            self.orders.add(order)
            self.save()
        else:
            order.quantity += quantity
            order.save()
        return True

    def total(self):
        total = 0
        for order in self.orders.all():
            total += order.product.price * order.quantity

        return total

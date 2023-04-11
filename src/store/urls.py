from django.urls import path

from .views import *

app_name = "store"

urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductsListView.as_view(), name="products-list"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("product/<slug:slug>/add-to-cart/", add_to_cart, name="add-to-cart"),

    path("cart/", cart, name="cart"),
    path("cart/update-quantities/", update_quantities, name="update-quantities"),
    path("cart/delete-order/<slug:slug>", delete_order, name="delete-order"),
    path("cart/delete/", delete_cart, name="delete-cart"),

    path("cart/create-checkout-session/", create_checkout_session, name="create-checkout-session"),
    path("cart/success/", checkout_success, name="checkout-success"),
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),

]

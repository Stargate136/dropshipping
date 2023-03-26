from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

import stripe

from shop import settings
from . import models, forms

User = get_user_model()

stripe.api_key = settings.STRIPE_API_KEY


# Create your views here.
def index(request):
    return render(request, "store/index.html")


class ProductsListView(ListView):
    model = models.Category
    template_name = "store/products.html"
    context_object_name = "categories"


class ProductDetailView(DetailView):
    model = models.Product
    template_name = "store/detail.html"
    context_object_name = "product"


def add_to_cart(request, slug):
    user = request.user
    cart, _ = models.Cart.objects.get_or_create(user=user)
    done = cart.add_product(slug)
    if done:
        messages.add_message(request, messages.INFO, "L'article a été ajouté au panier.")
    else:
        messages.add_message(request, messages.INFO, "Une erreur s'est produite... Veuillez réessayer ultérieurement.")

    return redirect(reverse("store:product-detail", kwargs={"slug": slug}))


@login_required
def cart(request):
    orders = models.Order.objects.filter(user=request.user, ordered=False)
    if orders.count() == 0:
        return redirect(reverse("store:index"))
    OrderFormSet = modelformset_factory(models.Order, form=forms.OrderForm, extra=0)
    formset = OrderFormSet(queryset =orders)
    return render(request, "store/cart.html", context={"forms": formset})


def update_quantities(request):
    queryset = models.Order.objects.filter(user=request.user, ordered=False)
    OrderFormSet = modelformset_factory(models.Order, form=forms.OrderForm, extra=0)
    formset = OrderFormSet(request.POST, queryset=queryset)
    if formset.is_valid():
        formset.save()
    return redirect(reverse("store:cart"))


def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
    return redirect(reverse("store:index"))


def create_checkout_session(request):
    cart = request.user.cart

    line_items = [{"price": order.product.stripe_id,
                   "quantity": order.quantity} for order in cart.orders.all()]

    checkout_data = {"locale": "fr",
                     "shipping_address_collection": {"allowed_countries": ["FR"]},
                     "line_items": line_items,
                     "mode": "payment",
                     "payment_method_types": ["card"],
                     "success_url": request.build_absolute_uri(reverse("store:checkout-succes")),
                     "cancel_url": request.build_absolute_uri(reverse("store:cart"))}
    if request.user.stripe_id:
        checkout_data["customer"] = request.user.stripe_id
    else:
        checkout_data["customer_creation"] = "always"
        checkout_data["customer_email"] = request.user.email

    session = stripe.checkout.Session.create(**checkout_data)

    return redirect(session.url, code=303)


def checkout_succes(request):
    return render(request, "store/succes.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.ENDPOINT_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Passed signature verification

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        try:
            user_email = session["customer_details"]["email"]
            user = get_object_or_404(User,
                                     email=user_email)
        except KeyError:
            return HttpResponse("Invalid user email", status=404)

        user.complete_order(customer_id=session["customer"])
        user.save_shipping_address(address=session["shipping_details"]["address"],
                                   name=session["shipping_details"]["name"])
        return HttpResponse(status=200)

    return HttpResponse(status=400)


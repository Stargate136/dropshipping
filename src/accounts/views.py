from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from . import forms
from . import models


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data["email"],
                                password=form.cleaned_data["password1"])
            login(request, user)
            print("inscrit")
            return redirect(reverse("store:index"))
        else:
            return render(request, "accounts/signup.html", context={"form": form})

    form = forms.UserRegistrationForm()
    return render(request, "accounts/signup.html", context={"form": form})

def login_user(request):
    if request.method == "POST":
        form = forms.UserLoginForm(request, data=request.POST)
        if form.is_valid():
            form.clean()
            user = form.get_user()
            if user:
                login(request, user)
                return redirect(reverse("store:index"))
        else:
            return render(request, "accounts/login.html", context={"form": form})

    form = forms.UserLoginForm()
    return render(request, "accounts/login.html", context={"form": form})


def logout_user(request):
    logout(request)
    return redirect(reverse("store:index"))

@login_required
def profile(request):
    if request.method == "POST":
        post = request.POST
        is_valid = authenticate(email=post.get("email"), password=post.get("password"))
        if is_valid:
            user = request.user
            user.first_name = post.get("first_name")
            user.last_name = post.get("last_name")
            user.save()
            messages.add_message(request, messages.INFO, "Le profil a bien été modifié")
        else:
            messages.add_message(request, messages.ERROR, "Le mot de passe n'est pas valide.")
        return redirect(reverse("accounts:profile"))

    form = forms.UserForm(initial=model_to_dict(request.user, exclude="password"))
    addresses = request.user.addresses.all()
    return render(request, "accounts/profile.html", context={"form": form,
                                                             "addresses": addresses})

@login_required
def set_default_shipping_address(request, pk):
    address: models.ShippingAddress = get_object_or_404(models.ShippingAddress, pk=pk)
    address.set_default()
    return redirect("accounts:profile")

@login_required
def modify_address(request, pk):

    if request.method == "POST":
        post = request.POST
        is_valid = authenticate(email=post.get("email"),
                                password=post.get("password"))
        if is_valid:
            address = get_object_or_404(models.ShippingAddress, pk=pk)

            address.alias = post["alias"]
            address.name = post["name"]
            address.address_1 = post["address_1"]
            address.address_2 = post["address_2"]
            address.city = post["city"]
            address.zip_code = post["zip_code"]
            address.country = post["country"]

            address.save()

            return redirect("accounts:profile")

        else:
            messages.add_message(request, messages.ERROR, "Mot de passe incorrect.")


    address = get_object_or_404(models.ShippingAddress, pk=pk)

    data = model_to_dict(address)
    data["email"] = request.user.email

    form = forms.AddressForm(initial=data)

    return render(request, "accounts/modify_address.html", context={"form": form})

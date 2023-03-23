from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name="profile"),
    path("profile/set-default-shipping/<int:pk>/",
         set_default_shipping_address, name="set-default-shipping"),
    path("profile/modify-address/<int:pk>/", modify_address, name="modify-address"),
]

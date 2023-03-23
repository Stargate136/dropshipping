from django import forms

from . import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ["quantity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = [(i, i) for i in range(1, 99)]
        self.fields["quantity"] = forms.ChoiceField(choices=choices)
        self.fields["delete"] = forms.BooleanField(initial=False,
                                                   required=False,
                                                   label="Supprimer")
        
    def save(self, *args, **kwargs):
        if self.cleaned_data["delete"]:
            self.instance.delete()
            if self.instance.user.cart.orders.count() == 0:
                return self.instance.user.cart.delete()
            
        return super().save(*args, **kwargs)

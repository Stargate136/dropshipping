from django import forms

from . import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ["quantity"]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["decrement"] = forms.CharField(label="",
                                                   required=False,
                                                   widget=forms.TextInput(attrs={'type': 'submit',
                                                                                 'value': '-',
                                                                                 "class": "cta",
                                                                                 "data-role": "decrement"}))
        self.fields["quantity"] = forms.CharField(label="",
                                                  widget=forms.TextInput(attrs={'readonly': True,
                                                                                "value": self.instance.quantity,
                                                                                "class": "quantity-value",
                                                                                "data-role": "value"}))
        self.fields["increment"] = forms.CharField(label="",
                                                   required=False,
                                                   widget=forms.TextInput(attrs={'type': 'submit',
                                                                                 'value': '+',
                                                                                 "class": "cta",
                                                                                 "data-role": "increment"}))



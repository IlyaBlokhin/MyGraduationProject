from django import forms

DISH_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddDishForm(forms.Form):
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

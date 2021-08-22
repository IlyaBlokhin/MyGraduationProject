# Create your views here.

from django.shortcuts import redirect, get_object_or_404, render, HttpResponse
from django.views.decorators.http import require_POST
from mainApp.models import Dish

from .cart import Cart
from .forms import CartAddDishForm


@require_POST
def cart_add(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    form = CartAddDishForm(request.POST)
    remove_ingredients = request.POST['removeingredients']
    if ',' in remove_ingredients:
        remove_ingredients = remove_ingredients.split(',')
    else:
        remove_ingredients = [remove_ingredients]
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(dish=dish, remove_ingredients=remove_ingredients, quantity=1, update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, dish_id):
    cart = Cart(request)
    cart.remove(dish_id)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'detail.html', {'cart': cart})


def cart_update(request):
    return HttpResponse(f'{len(Cart(request))}')

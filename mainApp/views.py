from datetime import datetime

from cart.cart import Cart
from django.shortcuts import render, get_object_or_404, redirect

from .forms import OrderForm, PayOrder, UserRegistrationForm
from .models import Dish, DishType, OrderedDish, Order, Deal


# Create your views here.
def home(request):
    current_deals = []
    all_dishes = Dish.objects.all()
    all_categories = DishType.objects.all()
    page_title = 'My site'
    all_deals = Deal.objects.all()
    for el in all_deals:
        if el.start_date.date() <= datetime.today().date() <= el.stop_date.date():
            current_deals.append(el)
    deals_count = range(len(current_deals))
        if current_deals:
        first_deal = current_deals[0]
    else:
        first_deal = ''
    current_deals = all_deals[1::]

    return render(request, 'some_content.html', {'dishes': all_dishes, 'categories': all_categories, 'page_title': page_title, 'deals': current_deals, 'deals_count': deals_count, 'first_deal': first_deal})


def dish_cart(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    ing = dish.ingredients.all()
    page_title = 'Cart'
    return render(request, 'testjs.html',
                  {'dish': dish, 'ingredients': ing, 'page_title': page_title})


def make_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            if request.user.is_authenticated:
                request.user.orders.add(order)
            for item in cart:
                if item['remove_ingredients']:
                    if ',' in item['remove_ingredients']:
                        item['remove_ingredients'] = item['remove_ingredients'].split(', ')
                    else:
                        item['remove_ingredients'] = [item['remove_ingredients']]
                od = OrderedDish()
                od.order = order
                od.dish = item['dish']
                od.price = item['price']
                od.quantity = item['quantity']
                od.save()
                if item['remove_ingredients']:
                    od.remove_ingredients.add(*item['remove_ingredients'])
            cart.clear()
            return render(request, 'order/created.html',
                          {'order': order})
        else:
            form = OrderForm(request.POST)
    else:
        form = OrderForm(auto_id=False)
    if request.user.is_authenticated:
        total_price = (cart.get_total_price() * (100 - request.user.profile.get_discount())) / 100
    else:
        total_price = cart.get_total_price()
    return render(request, 'order/create.html',
                  {'cart': cart, 'form': form, 'total_price': total_price})


def profile(request):
    return render(request, 'profile.html')


def pay(request, order_number):
    order = get_object_or_404(Order, pk=order_number)
    print(order)
    if request.method == 'POST':
        form = PayOrder(request.POST)
        if form.is_valid():
            if form.cleaned_data['paid'] == True:
                order.paid = True
                order.save()
                return redirect('profile')
        else:
            form = PayOrder(request.POST)
    else:
        form = PayOrder()
    return render(request, 'pay.html', {'order': order, 'form': form})


def user_registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return redirect('login')
        else:
            user_form = UserRegistrationForm(request.POST)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

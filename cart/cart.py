from decimal import Decimal

from django.conf import settings
from mainApp.models import Dish


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, dish, add_ingredients='', remove_ingredients='', quantity=1, update_quantity=False):
        dish_id = str(dish.id)
        dish_cart_id = str(hash(dish_id + str(sorted(remove_ingredients))))
        if dish_cart_id not in self.cart:
            self.cart[dish_cart_id] = {'dishid': dish_id, 'quantity': 0, 'price': str(dish.price), 'add_ingredients': add_ingredients, 'remove_ingredients': ', '.join(remove_ingredients)}
        self.cart[dish_cart_id]['quantity'] += quantity
        self.save()

    def remove(self, dish_main_id, quantity=0):
        if dish_main_id in self.cart:
            if quantity == 0:
                del self.cart[dish_main_id]
            else:
                self.cart[dish_main_id] -= quantity
            self.save()

    def __iter__(self):
        dish_ids = [el['dishid'] for el in self.cart.values()]

        dishes = Dish.objects.filter(id__in=dish_ids)

        for key in self.cart:
            self.cart[key]['cart_id'] = key

        for el in self.cart.values():
            el['dish'] = dishes.get(id=el['dishid'])

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

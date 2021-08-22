from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class DishType(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Dish(models.Model):
    image = models.ImageField(upload_to='uploads')
    type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name='Dishes')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.ManyToManyField('Ingredient', related_name='Dishes')
    changes = models.OneToOneField('DishChange', on_delete=models.CASCADE, related_name='Dish')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class DishChange(models.Model):
    pass


class Ingredient(models.Model):
    INGREDIENT_TYPES = (('v', 'vegan'), ('m', 'meat'))

    title = models.CharField(max_length=50, primary_key=True)
    image = models.ImageField(upload_to='uploads')
    type = models.CharField(max_length=1, choices=INGREDIENT_TYPES)

    def __str__(self):
        return self.title


class OrderedDish(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    remove_ingredients = models.ManyToManyField(Ingredient, null=True, related_name='OrderedDishes', blank=True)

    def __str__(self):
        return f'Changed {self.dish}'

    def get_cost(self):
        return self.price * self.quantity


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.SmallAutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')

    def __str__(self):
        return f'Order {self.number} {self.get_total_cost()}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class Deal(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True)
    sub_title = models.CharField(max_length=250)
    comment = models.TextField()
    dishes = models.ManyToManyField('Dish', related_name='Deals')
    percent = models.PositiveIntegerField()
    promo_code = models.CharField(max_length=20)
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def get_discount(self):
        if not self.user.orders.filter(paid=True):
            discount = 30
        else:
            discount = 0
        tc = self.get_total_check()
        if 100 <= tc <= 200:
            discount = 5
        elif tc >= 200:
            discount = 10
        return discount


    def get_total_check(self):
        print(f'PRINT {self.user.orders.all()}')
        return sum([el.get_total_cost() if el.paid else 0 for el in self.user.orders.all()])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

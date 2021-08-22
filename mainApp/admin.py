from django.contrib import admin

from .models import Dish, Ingredient, Order, Deal, DishType, DishChange, OrderedDish, Profile

# Register your models here.
admin.site.register(Dish)
admin.site.register(Ingredient)

admin.site.register(OrderedDish)
admin.site.register(Deal)
admin.site.register(DishType)
admin.site.register(DishChange)


class OrderItemInline(admin.TabularInline):
    model = OrderedDish
    raw_id_fields = ['dish']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'first_name', 'email', 'paid', 'created_date']
    list_filter = ['paid', 'created_date']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Profile)

from django.contrib import admin


from .models import Salad, Subs, Pizza, Pasta, Orders, Toppings

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Toppings)

admin.site.register(Pasta)
admin.site.register(Subs)
admin.site.register(Salad)
admin.site.register(Orders)


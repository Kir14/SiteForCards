from django.contrib import admin

from .models import Client, Card, SecurityUser, Felial, Account, TypesCard

# Register your models here.

admin.site.register(SecurityUser)
admin.site.register(Felial)
admin.site.register(Account)
admin.site.register(TypesCard)
admin.site.register(Client)
admin.site.register(Card)

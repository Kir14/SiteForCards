from django.contrib import admin
from django.db.models import Count, Sum

from .models import Sending, Client, Card, SecurityUser, Felial, Account, TypesCard, SaleSummary


# Register your models here.

# admin.site.register(SecurityUser)
# admin.site.register(Felial)
# admin.site.register(Account)
# admin.site.register(TypesCard)
# admin.site.register(Client)
# admin.site.register(Card)
# admin.site.register(Sending)

@admin.register(SecurityUser)
class SecurityAdmin(admin.ModelAdmin):
    list_display = ('user', 'passport_num')


@admin.register(Felial)
class FelialAdmin(admin.ModelAdmin):
    list_display = ('numFelial', 'address', 'phone')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('numAccount', 'felial', 'user')


@admin.register(TypesCard)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('nameCard', 'price', 'description', 'ccy', 'cashback', 'validity_period', 'image')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'avatar')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('numCard', 'dateFinish', 'bankAccount', 'typeCard', 'image')


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ('card', 'sender', 'address', 'num_send', 'status')


@admin.register(SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    date_hierarchy = 'dateOFF'


class SendingSummaryAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            'total': Count('card'),
            'total_sales': Sum('card.typeCard.price'),
        }
        response.context_data['summary'] = list(
            qs
                .values('card.typeCard.nameCard')
                .annotate(**metrics)
                .order_by('-total_sales')
        )
        return response

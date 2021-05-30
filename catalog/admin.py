from django.contrib import admin
from django.db.models import Count, Sum, DateTimeField, Min, Max, DateField
from django.db.models.functions import Trunc

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


def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'


@admin.register(SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    date_hierarchy = 'dateOFF'

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
            'total': Count('id'),
            'total_sales': Sum('card__typeCard__price'),
        }
        response.context_data['summary'] = list(
            qs
                .values('card__typeCard__nameCard')
                .annotate(**metrics)
                .order_by('-total')
        )

        response.context_data['summary_total'] = dict(qs.aggregate(**metrics))

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period
        summary_over_time = qs.annotate(
            period=Trunc('dateOFF', 'day', output_field=DateField()),
        ).values('period') \
            .annotate(total=Count('card__typeCard__nameCard')) \
            .order_by('period')

        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)
        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': \
                (x['total'] or 0)  / (high) * 100
                if high > low else 0,
        } for x in summary_over_time]

        return response

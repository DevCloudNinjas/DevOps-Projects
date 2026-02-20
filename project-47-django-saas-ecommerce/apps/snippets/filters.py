
from django_filters import rest_framework as rfilters
from .models import Sales

from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from datetime import date


class SalesFilter(rfilters.FilterSet):

    class Meta:
        model = Sales
        fields = ['id', 'region', 'country', 'ptype', 'channel', 'date', 'quantity',
                  'price', 'cost', 'revenue', 'profit']

    # Defining minimum and maximum value filters in a row for numeric fields to be used in filtering as
    # "is_less_than_or_equal_to" and "is_greater_than_or_equal_to"
    for field in ['quantity', 'price', 'cost', 'revenue', 'profit', 'profit_percentage']:
        exec(f'min_{field} = rfilters.NumberFilter(field, lookup_expr="gte")')
        exec(f'max_{field} = rfilters.NumberFilter(field, lookup_expr="lte")')

    # filter by date as "is_less_than_or_equal_to"
    date_to = rfilters.CharFilter(method='m_date_to', label='date_to')

    # filter by date as "is_greater_than_or_equal_to"
    date_from = rfilters.CharFilter(method='m_date_from', label='date_from')

    # filter by exact date
    date = rfilters.CharFilter(method='date_exact', label='date')

    def date_exact(self, queryset, name, value):
        day, month, year = self.date_split(value)
        cdate = date(year, month, day)
        print(queryset)
        return queryset.filter(date=cdate)

    def m_date_to(self, queryset, name, value):
        day, month, year = self.date_split(value)
        cdate = date(year, month, day)
        return queryset.filter(date__lte=cdate)

    def m_date_from(self, queryset, name, value):
        day, month, year = self.date_split(value)
        cdate = date(year, month, day)
        return queryset.filter(date__gte=cdate)

    # Helper method to split a string by '.'
    def date_split(self, value):
        return [int(x) for x in value.split('.')]

    # Allow us to group by one or more columns: region, country, ptype, channel and date (not numeric columns)
    # with a result of total values of quantity, price, cost, revenue, profit and
    # calculated profit_percentage of total revenue and calculated profit
    groupby = rfilters.CharFilter(method='groupby_filter', label='groupby')

    def groupby_filter(self, queryset, name, value):

        return queryset.values(*self.request.query_params.getlist('groupby')).annotate(
            quantity=Sum('quantity'),
            price=Sum('price'),
            cost=Sum('cost'),
            revenue=Sum('revenue'),
            profit=Sum('profit'),
            profit_percentage=ExpressionWrapper(
                (F('profit')/F('revenue')) * 100, output_field=DecimalField())
        )
from app.models import UnitPrice


class UnitPriceService:

    def get_all_unit_prices(self):
        return UnitPrice.objects.all()

    def filter_unit_prices(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_all_unit_prices()
        return queryset.filter(**kwargs)

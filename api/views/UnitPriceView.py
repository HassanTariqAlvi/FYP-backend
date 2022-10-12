from api.serializers.UnitPriceSerializer import UnitPriceSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import UnitPrice
from app.services.BaseService import BaseService


class UnitPriceView(AbstractBaseView):
    model = UnitPrice
    queryset = UnitPrice.objects.all()
    serializer_class = UnitPriceSerializer
    post_message = "New unit price added successfully!"
    put_message = "Unit price updated successfully!"
    delete_message = "Unit price deleted successfully!"

    def create(self, request, *args, **kwargs):
        if request.data is not None:
            keys = request.data.keys()
            if 'unit' in keys:
                request.data['unit'] = BaseService.get_instance(
                    'Unit', name=request.data['unit']
                ).id
            if 'department' in keys:
                request.data['department'] = BaseService.get_instance(
                    'Department', name=request.data['department']
                ).id
            if 'criteria' in keys:
                request.data['criteria'] = BaseService.get_instance(
                    'MeasureCriteria', name=request.data['criteria']
                ).id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data is not None:
            keys = request.data.keys()
            if 'unit' in keys:
                request.data['unit'] = BaseService.get_instance(
                    'Unit', name=request.data['unit']
                ).id
            if 'department' in keys:
                request.data['department'] = BaseService.get_instance(
                    'Department', name=request.data['department']
                ).id
            if 'criteria' in keys:
                request.data['criteria'] = BaseService.get_instance(
                    'MeasureCriteria', name=request.data['criteria']
                ).id
        return super().update(request, *args, **kwargs)

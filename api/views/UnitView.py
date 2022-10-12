from api.serializers.UnitSerializer import UnitSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import Unit


class UnitView(AbstractBaseView):
    model = Unit
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    post_message = "New unit added successfully!"
    put_message = "Unit updated successfully!"
    delete_message = "Unit deleted successfully!"

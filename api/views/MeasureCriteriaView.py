from api.serializers.MeasureCriteriaSerializer import MeasureCriteriaSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import MeasureCriteria


class MeasureCriteriaView(AbstractBaseView):
    model = MeasureCriteria
    queryset = MeasureCriteria.objects.all()
    serializer_class = MeasureCriteriaSerializer
    post_message = "Measure criteria created successfully!"
    put_message = "Measure criteria updated successfully!"
    delete_message = "Measure criteria deleted successfully!"

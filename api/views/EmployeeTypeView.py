from api.serializers.EmployeeTypeSerializer import EmployeeTypeSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import EmployeeType


class EmployeeTypeView(AbstractBaseView):
    model = EmployeeType
    queryset = EmployeeType.objects.all()
    serializer_class = EmployeeTypeSerializer
    post_message = "Employee type created successfully!"
    put_message = "Employee type updated successfully!"
    delete_message = "Employee type deleted successfully!"

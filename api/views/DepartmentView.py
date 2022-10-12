from api.serializers.DepartmentSerializer import DepartmentSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import Department


class DepartmentView(AbstractBaseView):
    model = Department
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    post_message = "Department created successfully!"
    put_message = "Department updated successfully!"
    delete_message = "Department deleted successfully!"

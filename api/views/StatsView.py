from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Employee
from django.db.models import Count


class StatsView(APIView):
    def __extract_data(self, queryset):
        labels = []
        values = []
        for record in queryset:
            labels.append(record['employee_type__name'])

        for record in queryset:
            values.append(record['count'])

        return labels, values

    def get(self, request, *args, **kwargs):
        data = Employee.objects.values(
            'employee_type__name').annotate(count=Count('employee_type'))
        labels, values = self.__extract_data(data)
        return Response({
            'labels': labels,
            'values': values
        })

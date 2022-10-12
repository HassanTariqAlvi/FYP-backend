from api.serializers.ReportSerializer import DailyWorkReportSerializer, SalaryReportSerializer, AttendanceReportSerializer
from app.services.ReportService import ReportService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.exceptions import DoesNotExist


class ReportsView(APIView):

    def post(self, request, *args, **kwargs):
        reportType = ""

        if request.data is None or 'report_type' not in request.data.keys():
            raise DoesNotExist(detail="Please select report type.")

        reportType = request.data['report_type']
        report_service = ReportService()        

        if reportType == "Daily Work report":
            serializer = DailyWorkReportSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            data = report_service.get_dailywork_report(data)

        elif reportType == "Attendance report":
            serializer = AttendanceReportSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            data = report_service.get_attendance_report(data)

        elif reportType == "Salaries report":
            serializer = SalaryReportSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            data = report_service.get_salary_report(data)

        return Response({
            'status_code': status.HTTP_200_OK,
            'data': data['data'],
            # 'data': [],
            'columns': data['columns'],
            # 'columns': [],
        })

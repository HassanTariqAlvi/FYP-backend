import csv

from api.serializers.LogFileSerializer import LogFileSerializer
from app.models import ReversionVersion
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.LogFileSerializer import LogFileSerializer
from rest_framework import status


class LogFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ReversionVersion.objects.all()
        serializer = LogFileSerializer(data, many=True)

        data_file = open('log_file.csv', 'w')
        csv_writer = csv.writer(data_file)
        count = 0

        for emp in serializer.data:
            if count == 0:
                header = emp.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(emp.values())

        data_file.close()
        return Response({'status_code': status.HTTP_200_OK, 'message': 'Log file generated successfully!'})

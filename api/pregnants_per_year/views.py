from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.pregnants_per_year.models import PregnantsPerYear


class PregnantsPerYearList(APIView):
    def get(self, request):
        pregnants_data = PregnantsPerYear.objects()
        data = []
        for record in pregnants_data:
            data.append({
                '_id': str(record._id),
                'total_count': record.total_count,
                'pregnant_count': record.pregnant_count,
                'percentage_pregnant': record.percentage_pregnant,
                'year': record.year,
            })
        return Response(data, status=status.HTTP_200_OK)

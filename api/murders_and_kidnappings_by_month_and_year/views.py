from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from historias_de_la_memoria.constants import MONTH_NAMES
from api.murders_and_kidnappings_by_month_and_year.models import MurdersAndKidnappingsByMonthAndYear


class MurdersAndKidnappingsByMonthAndYearList(APIView):
    def get(self, request):
        data_records = MurdersAndKidnappingsByMonthAndYear.objects()
        data = []
        for record in data_records:
            data.append({
                '_id': str(record._id),
                'murders_count': record.murders_count,
                'kidnappings_count': record.kidnappings_count,
                'year': record.year,
                'month': MONTH_NAMES[record.month],
            })
        return Response(data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.militancy_by_month_and_year.models import MilitancyByMonthAndYear
from historias_de_la_memoria.constants import MONTH_NAMES
from api.decorators import token_required


class MilitancyByMonthAndYearList(APIView):
    @token_required
    def get(self, request):
        militancy_data = MilitancyByMonthAndYear.objects()
        data = []
        for militancy in militancy_data:
            data.append({
                '_id': str(militancy._id),
                'year': militancy.year,
                'month': MONTH_NAMES[militancy.month],
                'with_militancy': militancy.with_militancy,
                'without_militancy': militancy.without_militancy,
            })
        return Response(data, status=status.HTTP_200_OK)

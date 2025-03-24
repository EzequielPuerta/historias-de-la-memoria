from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.nationalities_amount.models import NationalitiesAmount


class NationalitiesAmountList(APIView):
    def get(self, request):
        nationalities_data = NationalitiesAmount.objects()
        data = []
        for record in nationalities_data:
            data.append({
                '_id': str(record._id),
                'count': record.count,
                'nationality': record.nationality,
            })
        return Response(data, status=status.HTTP_200_OK)

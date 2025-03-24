from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend_api.min_and_max_ages.models import MinAndMaxAges


class MinAndMaxAgesList(APIView):
    def get(self, request):
        ages_data = MinAndMaxAges.objects()
        data = []
        for ages in ages_data:
            data.append({
                '_id': str(ages._id),
                'min_age': ages.min_age,
                'max_age': ages.max_age,
            })
        return Response(data, status=status.HTTP_200_OK)

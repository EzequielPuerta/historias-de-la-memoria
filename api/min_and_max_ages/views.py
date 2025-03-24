from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.min_and_max_ages.models import MixAndMaxAges
from api.decorators import token_required


class MixAndMaxAgesList(APIView):
    @token_required
    def get(self, request):
        ages_data = MixAndMaxAges.objects()
        data = []
        for ages in ages_data:
            data.append({
                '_id': str(ages._id),
                'min_age': ages.min_age,
                'max_age': ages.max_age,
            })
        return Response(data, status=status.HTTP_200_OK)

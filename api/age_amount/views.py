from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.age_amount.models import AgeAmount


class AgeAmountList(APIView):
    def get(self, request):
        age_amounts = AgeAmount.objects()
        data = []
        for age_amount in age_amounts:
            data.append({
                '_id': str(age_amount._id),
                'from': age_amount._from,
                'to': age_amount._to,
                'count': age_amount.count,
            })
        return Response(data, status=status.HTTP_200_OK)

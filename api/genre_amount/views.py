from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.genre_amount.models import GenreAmount
from api.decorators import token_required


class GenreAmountList(APIView):
    @token_required
    def get(self, request):
        genre_amounts = GenreAmount.objects()
        data = []
        for genre_amount in genre_amounts:
            data.append({
                '_id': str(genre_amount._id),
                'count': genre_amount.count,
                'genre': genre_amount.genre,
            })
        return Response(data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.genre_amount.models import GenreAmount


class GenreAmountList(APIView):
    def get(self, request):
        genre_amounts = GenreAmount.objects()
        data = []
        for genre_amount in genre_amounts:
            data.append({
                '_id': str(genre_amount._id),
                'count': genre_amount.count,
                'genre': genre_amount.genre if genre_amount.genre else 'Desconocido',
            })
        return Response(data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend_api.genre_amount_by_year.models import GenreAmountByYear


class GenreAmountByYearList(APIView):
    def get(self, request):
        genre_amounts_by_year = GenreAmountByYear.objects()
        data = []
        for genre_amount in genre_amounts_by_year:
            data.append({
                '_id': str(genre_amount._id),
                'year': genre_amount.year,
                'male_count': genre_amount.male_count,
                'female_count': genre_amount.female_count,
            })
        return Response(data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.constants import MONTH_NAMES
from backend_api.published.models import Published


class PublishedList(APIView):
    def get(self, request):
        published_data = Published.objects()
        data = []
        for record in published_data:
            data.append({
                '_id': str(record._id),
                'day': record.day,
                'month': MONTH_NAMES[record.month],
                'desaparecidos': record.desaparecidos,
            })
        return Response(data, status=status.HTTP_200_OK)

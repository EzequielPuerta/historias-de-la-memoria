from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.murders_and_kidnappings.models import MurdersAndKidnappings


class MurdersAndKidnappingsList(APIView):
    def get(self, request):
        murders_and_kidnappings = MurdersAndKidnappings.objects()
        data = []
        for record in murders_and_kidnappings:
            data.append({
                '_id': str(record._id),
                'count': record.count,
                'fact_type': record.fact_type,
            })
        return Response(data, status=status.HTTP_200_OK)

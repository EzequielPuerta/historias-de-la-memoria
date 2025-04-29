from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend_api.related_victims.models import RelatedVictim


class RelatedVictimsList(APIView):
    def get(self, request):
        related_victims_list = RelatedVictim.objects()
        data = []

        for related_victims in related_victims_list:
            relatives = []
            for each in related_victims.related_victims:
                relatives.append({
                    'relationship': each.relationship,
                    'victim': {
                        '_id': str(each.victim._id),
                        'name': each.victim.name,
                        'source_entry': {
                            'data_source': each.victim.source_entry.data_source,
                            'url': each.victim.source_entry.url,
                        }
                    }
                })
            data.append({
                '_id': str(related_victims._id),
                'name': related_victims.name,
                'source_entry': {
                    'data_source': related_victims.source_entry.data_source,
                    'url': related_victims.source_entry.url,
                },
                'photos': [{'type': photo.type.value, 'url': photo.url} for photo in related_victims.photos],
                'related_victims_count': related_victims.related_victims_count,
                'related_victims': relatives,
            })
        return Response(data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend_api.children_amount_by_year.models import ChildrenAmountByYear


class ChildrenAmountByYearList(APIView):
    def get(self, request):
        children_amounts_by_year = ChildrenAmountByYear.objects()
        data = []
        for children_amount in children_amounts_by_year:
            data.append({
                '_id': str(children_amount._id),
                'total_children': children_amount.total_children,
                'year': children_amount.year,
            })
        return Response(data, status=status.HTTP_200_OK)

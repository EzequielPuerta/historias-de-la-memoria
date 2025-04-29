from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "age-amount": reverse(
                "age-amount-list",
                request=request,
                format=format,
            ),
            "children-amount-by-year": reverse(
                "children-amount-by-year-list",
                request=request,
                format=format,
            ),
            "genre-amount": reverse(
                "genre-amount-list",
                request=request,
                format=format,
            ),
            "genre-amount-by-year": reverse(
                "genre-amount-by-year-list",
                request=request,
                format=format,
            ),
            "militancy-by-month-and-year": reverse(
                "militancy-by-month-and-year-list",
                request=request,
                format=format,
            ),
            "min-and-max-ages": reverse(
                "min-and-max-ages-list",
                request=request,
                format=format,
            ),
            "murders-and-kidnappings": reverse(
                "murders-and-kidnappings-list",
                request=request,
                format=format,
            ),
            "murders-and-kidnappings-by-month-and-year": reverse(
                "murders-and-kidnappings-by-month-and-year-list",
                request=request,
                format=format,
            ),
            "nationalities-amount": reverse(
                "nationalities-amount-list",
                request=request,
                format=format,
            ),
            "pregnants-per-year": reverse(
                "pregnants-per-year-list",
                request=request,
                format=format,
            ),
            "published": reverse(
                "published-list",
                request=request,
                format=format,
            ),
            "related-victims": reverse(
                "related-victims-list",
                request=request,
                format=format,
            ),
        }
    )

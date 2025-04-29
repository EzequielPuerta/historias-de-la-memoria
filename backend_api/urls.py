from django.urls import path
from backend_api.views import api_root
from backend_api.age_amount.views import AgeAmountList
from backend_api.children_amount_by_year.views import ChildrenAmountByYearList
from backend_api.genre_amount.views import GenreAmountList
from backend_api.genre_amount_by_year.views import GenreAmountByYearList
from backend_api.militancy_by_month_and_year.views import MilitancyByMonthAndYearList
from backend_api.min_and_max_ages.views import MinAndMaxAgesList
from backend_api.murders_and_kidnappings.views import MurdersAndKidnappingsList
from backend_api.murders_and_kidnappings_by_month_and_year.views import MurdersAndKidnappingsByMonthAndYearList
from backend_api.nationalities_amount.views import NationalitiesAmountList
from backend_api.pregnants_per_year.views import PregnantsPerYearList
from backend_api.published.views import PublishedList
from backend_api.related_victims.views import RelatedVictimsList


urlpatterns = [
    path('', api_root),
    path('age-amounts/', AgeAmountList.as_view(), name='age-amount-list'),
    path('children-amounts-by-year/', ChildrenAmountByYearList.as_view(), name='children-amount-by-year-list'),
    path('genre-amounts/', GenreAmountList.as_view(), name='genre-amount-list'),
    path('genre-amounts-by-year/', GenreAmountByYearList.as_view(), name='genre-amount-by-year-list'),
    path('militancy-by-month-and-year/', MilitancyByMonthAndYearList.as_view(), name='militancy-by-month-and-year-list'),
    path('min-and-max-ages/', MinAndMaxAgesList.as_view(), name='min-and-max-ages-list'),
    path('murders-and-kidnappings/', MurdersAndKidnappingsList.as_view(), name='murders-and-kidnappings-list'),
    path('murders-and-kidnappings-by-month-and-year/', MurdersAndKidnappingsByMonthAndYearList.as_view(), name='murders-and-kidnappings-by-month-and-year-list'),
    path('nationalities-amounts/', NationalitiesAmountList.as_view(), name='nationalities-amount-list'),
    path('pregnants-per-year/', PregnantsPerYearList.as_view(), name='pregnants-per-year-list'),
    path('published/', PublishedList.as_view(), name='published-list'),
    path('related-victims/', RelatedVictimsList.as_view(), name='related-victims-list'),
]

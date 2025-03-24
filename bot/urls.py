from django.urls import path

from bot.views import execute_view


urlpatterns = [
    path('execute', execute_view),
]

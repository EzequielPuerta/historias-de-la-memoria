from django.urls import path

from historias_de_la_memoria_bot.views import index


urlpatterns = [
    path('', index),
]

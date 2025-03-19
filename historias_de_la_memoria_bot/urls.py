from django.urls import path

from historias_de_la_memoria_bot.views import index, execute_view


urlpatterns = [
    path('', index),
    path('bot/execute', execute_view),
]

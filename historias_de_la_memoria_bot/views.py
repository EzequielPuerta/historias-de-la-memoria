import os
from django.http import JsonResponse
from historias_de_la_memoria_bot.tasks.main import execute


def execute_view(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        if token != f"Bearer {os.environ.get('CRON_SECRET')}":
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        else:
            try:
                result = execute()
                return JsonResponse(result, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

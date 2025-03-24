import os
from django.http import JsonResponse


def token_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Bearer {os.environ.get('API_TOKEN')}":
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from datetime import datetime

from django.http import HttpResponse
from historias_de_la_memoria_bot.task import murdered


def index(request):
    now = datetime.now()
    disappeared = murdered()

    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
            <h2>Murdered Facts:</h2>
            <ul>
                {[f"<li>{each}</li>" for each in disappeared['results']]}
            </ul>
        </body>
    </html>
    '''
    return HttpResponse(html)

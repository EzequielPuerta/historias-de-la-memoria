from django.views.generic import TemplateView


class SPAView(TemplateView):
    template_name = "index.html"

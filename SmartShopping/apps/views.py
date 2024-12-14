from django.views.generic import TemplateView

from apps.product.models import ProductCollection

class HomeView(TemplateView):
    template_name = 'index.html'
    extra_context = {'title': "Home", "home": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ProductCollection.objects.filter(
            active=True, show_on_homepage=True
        )
        return context

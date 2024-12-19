from django.views.generic import ListView, DetailView

from apps.product.models import Product, ProductCollection


class ProductListView(ListView):
    template_name = 'product/list.html'
    queryset = Product.objects.filter(active=True)
    extra_context = {'title': "Products", "shop": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if category := self.request.GET.get('category'):
            context['category_id'] = int(category)
            context['shop'] = False
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if category := self.request.GET.get('category'):
            queryset = queryset.filter(category_id=category)
        return queryset


class ProductDetailView(DetailView):
    template_name = 'product/detail.html'
    queryset = Product.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_products = Product.objects.filter(active=True).exclude(
            id=self.object.id).order_by('?')[:4]
        context['related_products'] = related_products
        context['title'] = self.object.name
        return context


class ProductCollectionDetailView(DetailView):
    template_name = 'product/collection.html'
    model = ProductCollection
    extra_context = {"shop": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['collection_id'] = self.object.pk
        return context

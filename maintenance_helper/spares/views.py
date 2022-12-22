from django.urls import reverse_lazy
from django.views import generic as views

from maintenance_helper.spares.models import SparePart, Stock


class SparePartsListView(views.ListView):
    context_object_name = 'parts'
    model = SparePart
    fields = '__all__'
    template_name = 'spare_parts/parts-list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        pattern = self.request.GET.get('pattern')
        if pattern:
            queryset = queryset.filter(part_number__icontains=pattern)

        queryset = queryset.order_by('part_number')
        return queryset


class SparePartCreateView(views.CreateView):
    model = SparePart
    fields = '__all__'
    template_name = 'spare_parts/part-create.html'

    def get_success_url(self):
        return reverse_lazy('part details', kwargs={
            'pk': self.object.pk,
        })


class SparePartsDetailView(views.DetailView):
    model = SparePart
    exclude = ('part_number',)
    template_name = 'spare_parts/parts-details.html'


class SparePartEditView(views.UpdateView):
    model = SparePart
    fields = ('description', 'price', 'image')
    template_name = 'spare_parts/parts-edit.html'
    success_url = reverse_lazy('spare parts')

    def get_success_url(self):
        return reverse_lazy('part details', kwargs={
            'pk': self.object.pk,
        })


class SparePartDeleteView(views.DeleteView):
    pass


class StockItemsView(views.ListView):
    model = Stock
    fields = '__all__'
    template_name = 'spare_parts/stock_items_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('part_number')


class StockItemEdit(views.UpdateView):
    context_object_name = 'part'
    model = Stock
    fields = ('quantity', 'min_stock_qty')
    template_name = 'spare_parts/stock_item_edit.html'
    success_url = reverse_lazy('stock list')


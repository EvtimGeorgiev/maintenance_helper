from datetime import datetime

from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic as views
from maintenance_helper.orders.models import Order, OrderedItem, Cart
from maintenance_helper.spares.models import SparePart, Stock


class OrdersListView(views.ListView):
    model = Order
    template_name = 'orders/orders.html'
    ordering = ['order_number']


class AddToCart(views.ListView):
    model = SparePart
    template_name = 'orders/add_to_cart.html'
    fields = ('part_number', 'quantity')
    # form_class = CreateOrderForm
    search_pattern = ''

    def get(self, request, *args, **kwargs):
        if 'Add to cart' in request.GET and request.GET['part number']:
            part_number = request.GET['part number']
            try:
                qty = int(request.GET['qty'])
            except ValueError:
                return redirect('create oder')
            Cart.add_to_cart(part_number, qty)
            return redirect('create oder')

        elif 'Order' in request.GET:
            self.place_order()
            return redirect('orders list')

        return super().get(request, *args, **kwargs)

    @staticmethod
    def place_order():
        items_in_cart = Cart.objects.all()
        if not items_in_cart:
            return
        next_order_number = Order.get_next_order_number()
        new_order = Order.objects.create(order_number=next_order_number, total_price=Cart.get_total_price())

        for item in items_in_cart:
            spare_part = SparePart.objects.get(part_number=item.part_number)
            description = spare_part.description
            price = spare_part.price
            OrderedItem.objects.create(order_number=new_order, part_number=spare_part,
                                       description=description, quantity=item.quantity, price=price)
        Cart.empty_cart()

    def get_queryset(self):
        queryset = super().get_queryset()
        pattern = self.__get_pattern()
        if pattern:
            queryset = queryset.filter(part_number__icontains=pattern)
            self.extra_context = {'pattern': pattern}

        queryset = queryset.order_by('part_number')

        return queryset

    def __get_pattern(self):
        pattern = self.request.GET.get('pattern')
        return pattern if pattern else None
        #
        # def get_form(self, form_class=None):
        #     form = super().get_form(form_class)
        #     if search_pattern:
        #         form.fields['part_number'].queryset = SparePart.objects.filter(part_number__icontains=search_pattern)
        #     return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart_content'] = Cart.objects.all()
        context['total_cart_qty'] = context['cart_content'].count()

        return context


class ShowCartView(views.ListView):
    model = Cart
    template_name = 'orders/show_cart.html'
    ordering = ['part_number']

    def get(self, request, *args, **kwargs):
        if 'Update' in request.GET:
            pn_to_update = request.GET.get('Update')
            new_qty = int(request.GET.get(pn_to_update))
            ordered_item = self.model.objects.get(part_number=pn_to_update)
            if new_qty != ordered_item.quantity:
                ordered_item.quantity = new_qty
                ordered_item.save(update_fields=['quantity'])
            return redirect('show cart')

        elif 'Remove' in request.GET:
            pn_to_remove = request.GET.get('Remove')
            object_to_remove = self.model.objects.get(part_number=pn_to_remove)
            object_to_remove.delete()
            return redirect('show cart')

        elif 'Order' in request.GET:
            AddToCart.place_order()
            return redirect('orders list')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['ordered_items'] = Cart.objects.all()
        context['total_price'] = Cart.get_total_price()
        return context


class OrderDetailsView(views.DetailView):
    model = Order
    template_name = 'orders/order_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordered_items = self.get_ordered_items()
        context['ordered_items'] = ordered_items
        return context

    def get(self, request, *args, **kwargs):
        if 'Receive' in request.GET:
            pass
            ordered_items = self.get_ordered_items()
            if ordered_items:
                for item in ordered_items:
                    Stock.add_to_stock(part_number=item.part_number, quantity=item.quantity)
                order = self.get_object()
                order.received_on = datetime.today()
                order.save()

        return super().get(request, *args, **kwargs)

    def get_ordered_items(self):
        order = self.get_object()
        return OrderedItem.objects.filter(order_number_id=order.order_number)


class UpdateCartView(views.UpdateView):
    model = Cart

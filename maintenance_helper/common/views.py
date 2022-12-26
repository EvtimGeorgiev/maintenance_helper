from django.db.models import F
from django.shortcuts import render

from maintenance_helper.issues.models import Issue
from maintenance_helper.orders.models import Order
from maintenance_helper.spares.models import Stock


def index(request):
    issues = Issue.objects.all()[:5]
    open_orders_count = Order.objects.filter(received_on__isnull=True).count()
    items_below_min = Stock.objects.filter(quantity__lt=F('min_stock_qty')).count()

    context = {
        'issues': issues,
        'open_orders_count': open_orders_count,
        'items_below_min': items_below_min,
    }
    return render(request, 'base/index.html', context)


def access_denied(request):
    return render(request, 'base/access_denied.html')

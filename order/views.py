from django.shortcuts import render, redirect, get_object_or_404
from .models import Order


def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order/orders.html', {'orders': orders})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})
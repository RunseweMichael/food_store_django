import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from order.models import Order, OrderItem
from django.db import transaction
from menu.models import Menu
from .models import Cart, CartItem
from category.models import Category


def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


def add_to_cart(request, id):
    menu = get_object_or_404(Menu, id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, menu=menu)
    item.quantity += 1
    item.save()
    messages.success(request, f"{menu.name} added to cart.")
    return redirect('view_cart')


def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id, cart__user=request.user)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('view_cart')


def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()
    messages.success(request, f"Quantity of {item.menu.name} increased.")
    return redirect('view_cart')


def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        messages.info(request, f"Quantity of {item.menu.name} decreased.")
    else:
        item.delete()
        messages.warning(request, f"{item.menu.name} removed from cart.")
    return redirect('view_cart')



from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# @transaction.atomic
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    # Create order
    total = cart.total_price()
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status='PENDING',
    )

    # Build order items
    for item in cart.items.all():
        menu = item.menu

        # Check stock
        if item.quantity > menu.quantity:
            messages.error(request, f"Not enough stock for {menu.name}.")
            return redirect('view_cart')

        # Reduce stock
        menu.quantity -= item.quantity
        menu.save()

        # Reduce category total
        category = menu.category
        category.quantity -= item.quantity
        category.save()

        # Create order item
        OrderItem.objects.create(
            order=order,
            menu=menu,
            quantity=item.quantity,
            price=menu.price
        )

    # Clear cart
    cart.items.all().delete()

    # ✅ Send order confirmation email using SendGrid
    subject = f"Order #{order.id} Confirmation - The Food Hub"
    html_message = render_to_string('cart/order_confirmation.html', {'order': order, 'user': request.user})
    plain_message = strip_tags(html_message)

    message = Mail(
        from_email="runsewemichael93@gmail.com",  # This must be a verified sender in SendGrid
        to_emails=request.user.email,
        subject=subject,
        html_content=html_message
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        print("❌ Email send failed:", e)

    messages.success(request, f"Order #{order.id} created successfully! A confirmation email has been sent.")
    return redirect('order_detail', order_id=order.id)

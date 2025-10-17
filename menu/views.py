from django.shortcuts import render, redirect, get_object_or_404
from category.models import Category
from .models import Menu
from django.utils.text import slugify

# Create your views here.
def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'menu/menu_list.html', {'menus': menus})
        

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from .models import Menu
from category.models import Category

def create_menu_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category_id')

        # Validate category
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('create_menu_item')


    
        # Safely convert numeric fields
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            quantity = 0

        try:
            price = Decimal(price)
        except (ValueError, TypeError):
            price = Decimal('0.00')

        # Create new menu item
        Menu.objects.create(
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            image=image,
            category=category
        )

        category.quantity += quantity
        category.save()

        messages.success(request, f"Menu item '{name}' created successfully!")
        return redirect('menu_list')

    # For GET requests → show form
    categories = Category.objects.all()
    return render(request, 'menu/createMenuItem.html', {'categories': categories})



def delete_menu_item(request, id):
    menu_item = get_object_or_404(Menu, id=id)
    category = menu_item.category  # Get the related category

    if request.method == 'POST':
        # Reduce category quantity by menu item's quantity
        category.quantity -= menu_item.quantity
        if category.quantity < 0:
            category.quantity = 0  # Prevent negative quantities
        category.save()

        # Delete the menu item
        menu_item.delete()

        messages.success(
            request, 
            f"Menu item '{menu_item.name}' deleted successfully! Category '{category.name}' updated."
        )
        return redirect('menu_list')

    return render(request, 'menu/deleteMenuItem.html', {'menu_item': menu_item})



def update_menu_item(request, id):
    menu_item = get_object_or_404(Menu, id=id)
    old_quantity = menu_item.quantity
    old_category = menu_item.category

    if request.method == 'POST':
        menu_item.name = request.POST.get('name')
        menu_item.description = request.POST.get('description')
        menu_item.quantity = request.POST.get('quantity') or 0
        menu_item.price = request.POST.get('price') or 0
        category_id = request.POST.get('category_id')

        # Validate and assign new category
        try:
            new_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('update_menu_item', id=id)

        # Handle numeric fields safely
        try:
            menu_item.quantity = int(menu_item.quantity)
        except (ValueError, TypeError):
            menu_item.quantity = 0

        try:
            menu_item.price = Decimal(menu_item.price)
        except (ValueError, TypeError):
            menu_item.price = Decimal('0.00')

        # Handle image upload
        if 'image' in request.FILES:
            menu_item.image = request.FILES['image']

        # Adjust category quantities
        quantity_diff = menu_item.quantity - old_quantity

        if old_category.id == new_category.id:
            # Same category: just adjust by the difference
            old_category.quantity += quantity_diff
            if old_category.quantity < 0:
                old_category.quantity = 0
            old_category.save()
        else:
            # Different category: subtract from old, add to new
            old_category.quantity -= old_quantity
            if old_category.quantity < 0:
                old_category.quantity = 0
            old_category.save()

            new_category.quantity += menu_item.quantity
            new_category.save()

        # Assign the new category to the menu item
        menu_item.category = new_category
        menu_item.save()

        messages.success(request, f"Menu item '{menu_item.name}' updated successfully!")
        return redirect('menu_list')

    categories = Category.objects.all()
    return render(request, 'menu/updateMenuItem.html', {
        'menu_item': menu_item,
        'categories': categories
    })
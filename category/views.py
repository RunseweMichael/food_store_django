from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from django.utils.text import slugify

# Create your views here.
def category_list(request):
    Categories = Category.objects.all()
    return render(request, 'category/category.html', {'Categories': Categories})


def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    # Fetch 4 other random categories for the carousel (excluding current)
    related_categories = Category.objects.exclude(id=category.id).order_by('?')[:4]
    return render(request, 'category/category_detail.html', {
        'category': category,
        'related_categories': related_categories
    })



def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug') or slugify(name)
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Category.objects.create(
            name=name,
            slug=slug,
            description=description,
            image=image
        )
        return redirect('category_list')

    return render(request, 'category/createCategory.html')


def deletecategory(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('category_list')


def updatecategory(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.slug = request.POST.get('slug')
        category.description = request.POST.get('description')
        if 'image' in request.FILES:
            category.image = request.FILES['image']

        category.save()
        return redirect('category_list')  # make sure this URL name exists

    return render(request, 'category/updatecategory.html', {'category': category})
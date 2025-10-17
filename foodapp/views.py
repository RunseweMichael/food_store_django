from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import RegistrationForm, LoginForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.
def welcome(request):
    return render(request, 'foodapp/welcome.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            username = form.cleaned_data['username']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            age = form.cleaned_data['age']
            phone = form.cleaned_data['phone']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=firstName,
                last_name=lastName
            )

            UserProfile.objects.create(user=user, age=age, phone=phone)

            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'foodapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'foodapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@staff_member_required
def allusers(request):
    allusers = UserProfile.objects.select_related('user').all()
    return render(request, 'foodapp/allusers.html', {'allusers': allusers})


@staff_member_required
def deleteuser(request, id):
    userDelete = UserProfile.objects.get(pk=id)
    userDelete.delete()

    return redirect('allusers')


@staff_member_required
def updateuser(request, id):
    allusers = UserProfile.objects.get(pk=id)

    if request.method == 'POST':
        allusers.user.first_name = request.POST['fname']
        allusers.user.last_name = request.POST['lname']
        allusers.user.username = request.POST['uname']
        allusers.age = request.POST['age']
        allusers.phone = request.POST['phone']
        allusers.user.email = request.POST['email']
        
        allusers.user.save()
        allusers.save()

        return redirect('allusers')

    else:
        return render(request, 'foodapp/updateusers.html', context={'update': allusers})
    



@login_required
def home(request):
    return render(request, 'foodapp/home.html')


@login_required
def about(request):
    return render(request, 'foodapp/about.html')

@login_required
def contact(request):
    return render(request, 'foodapp/contact.html')
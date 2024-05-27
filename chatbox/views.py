from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from faker import Faker
from .models import User, Message

# Create your views here.

def get_random_username():
    fake = Faker().city()
    return fake
    

def signup(request):
    username = get_random_username()
    print(username)
    if request.method == 'POST':
        password = request.POST['password']
        user = User.objects.create(username=username) #type: ignore
        user.set_password(password)
        user.save()
        auth_login(request, user)
        return redirect('room')
    else:
        return render(request, 'signup.html', {'username': username})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'chat.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

@login_required  
def room(request):
    messages = Message.objects.all()
    return render(request, 'room.html', {'messages': messages})

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
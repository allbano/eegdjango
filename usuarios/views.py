from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib.messages import add_message
from django.contrib import auth

from django.http import HttpResponse

# Create your views here.
def home(request):
    if (request.method == "GET"):
        return render(request, 'home.html')
    

def cadastro(request):
    if (request.method == "GET"):
        return render(request, 'cadastro.html')
    elif (request.method == "POST"):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        users = User.objects.filter(username=username)
        if users.exists():
            add_message(request, constants.ERROR, 'Usuário ja existe!')
            return redirect('/usuarios/cadastro')

        if password != cpassword:
            add_message(request, constants.ERROR, 'As senhas precisam ser iguais!')
            return redirect('/usuarios/cadastro')
        if len(password) < 6:
            add_message(request, constants.ERROR, 'A senha deve ter mais que 6 dígitos!')
            return redirect('/usuarios/cadastro')
        
        try:
            User.objects.create_user(
                username = username, 
                first_name = first_name, 
                last_name = last_name, 
                email = email,
                password = password
            )
            return redirect('/usuarios/login')
        except:
            return redirect('/usuarios/cadastro') 

        return HttpResponse(f'{username}, {first_name}, {last_name}, {email}, {password}, {cpassword}')

def login(request):
    if (request.method == "GET"):
        print(request.user)
        return render(request, 'login.html')
    elif (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request,username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('/usuarios/home')
        
        add_message(request, constants.ERROR, 'Usuário ou senha inválidos!')
        return redirect('/usuarios/login')

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')
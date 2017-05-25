from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render,  redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from myApp.models import Profil, Utilisateur

def login_view(request):
    error = False
    me = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            activeuser = get_object_or_404(Profil, user=request.user)
            role = "admin"
            me = Utilisateur.objects.filter(personne=activeuser)
            user_profil = None
            if me.count() == 1:
                role = "utilisateur"
                user_profil = get_object_or_404(Utilisateur, personne=activeuser)
                #Mettre les identifiants de l'utilisateur dans une session


            #redirection vers la page d'accueil
            return redirect(reverse(home))
        else:
            error = True

    return render(request, 'login_page.html', locals())

def logout_view(request):
    logout(request)
    return redirect(reverse(login_view))

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html', locals())

@login_required(login_url='/login/')
def sendRequest(request):
    return render(request, 'send_request.html', locals())

@login_required(login_url='/login/')
def config(request):
    return render(request, 'config.html', locals())

@login_required(login_url='/login/')
def discover(request):
    return render(request, 'discover.html', locals())

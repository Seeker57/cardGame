from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Rarity, Card, Hero, HeroClass, CardClass, Player
from .forms import AuthForm, RegForm
# Create your views here.

def home(request):
    return render(request, "home.html")


def cards(request):
    cards = Card.objects.all()
    cardclass = CardClass.objects.all()
    return render(request, "cards.html", {"cards" : cards, "cardclass" : cardclass})


def usersCards(request, name):
    player = Player.objects.get(nickname=name)
    cards = player.cardplayer_set.all()
    return render(request, "cardsPlayer.html", {"player" : player, "cards" :cards})


def hero(request):
    heroes = Hero.objects.all()
    classes = HeroClass.objects.all()
    return render(request, "hero.html", {"heroes" : heroes, "classes" : classes})


def auth(request):
    if request.method == "POST":
        loginUser = request.POST.get("email")
        pswUser = request.POST.get("password")

        user = Player.objects.filter(login=loginUser)
        if user:
            if user[0].password == pswUser:
                return HttpResponseRedirect("/users/" + user[0].nickname)
            else:
                return HttpResponse("<h2>Неверный пароль для {0}</h2>".format(loginUser))
        else:
            return HttpResponse("<h2>Пользователь {0} не существует</h2>".format(loginUser))
    else:
        authform = AuthForm()
        return render(request, "auth.html", {"form": authform})
        

def reg(request):
    if request.method == "POST":
        newUser = Player()
        nicknameUser = request.POST.get("login")
        loginUser = request.POST.get("email")
        pswUser = request.POST.get("password")
        pswConfirmUser = request.POST.get("password")
        if (not Player.objects.filter(nickname=nicknameUser)) and (not Player.objects.filter(login=loginUser)) :
            if pswUser == pswConfirmUser:
                newUser.nickname = nicknameUser
                newUser.login = loginUser
                newUser.password = pswUser
                newUser.resourses = 0
                newUser.save()
                return HttpResponseRedirect("/auth/")
            else:
                return HttpResponse("<h2>Пароли не совпадают</h2>")
        else:
            return HttpResponse("<h2>Пользователь с таким ником или email'ом уже существует")
    else:
        regForm = RegForm()
        return render(request, "auth.html", {"form" : regForm})

def users(request, name):
    return render(request, "home.html")
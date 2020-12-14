from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Rarity, Card, Hero, HeroClass, CardClass, Player, CardPlayer
from .forms import AuthForm, RegForm
# Create your views here.

def mainStr(request):
    return render(request, "main.html")

def home(request):
    return render(request, "home.html")


def cards(request):
    cards = Card.objects.all()
    cardclass = CardClass.objects.all()
    return render(request, "cards.html", {"cards" : cards, "cardclass" : cardclass})


def usersCards(request, name):
    player = Player.objects.filter(nickname=name)
    if player:
        cards = player[0].cardplayer_set.all()
        return render(request, "cardsPlayer.html", {"player" : player[0], "cards" :cards})
    else:
        return HttpResponse("<h2>Пользователь не найден</h2>")


def usersHeroes(request, name):
    player = Player.objects.filter(nickname=name)
    if player:
        heroes = player[0].heroplayer_set.all()
        return render(request, "heroUsers.html", {"player" : player[0], "heroes" : heroes})
    else:
        return HttpResponse("<h2>Пользователь не найден</h2>")


def usersDecks(request, name):
    player = Player.objects.filter(nickname=name)
    if player:
        decks = player[0].deck_set.all()
        return render(request, "decks.html", {"player" : player[0], "decks" : decks})
    else:
        return HttpResponse("<h2>Пользователь не найден</h2>")


def infoMessage(message):
    output = '<h2>' + message + '</h2>' +\
             '<form action="/" method="GET">' +\
             '<input type="submit" value="Вернуться на главную">' +\
             '</form>'
    return HttpResponse(output)


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
                mess = "Неверный пароль для {0}".format(loginUser)
                return infoMessage(mess)
        else:
            mess = "Пользователь {0} не существует".format(loginUser)
            return infoMessage(mess)
    else:
        authform = AuthForm()
        return render(request, "auth.html", {"form": authform})
        

def reg(request):
    if request.method == "POST":
        newUser = Player()
        nicknameUser = request.POST.get("login")
        loginUser = request.POST.get("email")
        pswUser = request.POST.get("password")
        pswConfirmUser = request.POST.get("passwordConfirm")
        if (not Player.objects.filter(nickname=nicknameUser)) and (not Player.objects.filter(login=loginUser)) :
            if pswUser == pswConfirmUser:
                newUser.nickname = nicknameUser
                newUser.login = loginUser
                newUser.password = pswUser
                newUser.resourses = 0
                newUser.save()
                allBeginsCards = Card.objects.filter(rarity=5)
                for card in allBeginsCards:
                    newLinkCardPlayer = CardPlayer()
                    newLinkCardPlayer.player = newUser
                    newLinkCardPlayer.card = card
                    newLinkCardPlayer.save()
                mess = "Аккаунт успешно создан"
                return infoMessage(mess)
            else:
                mess = "Пароли не совпадают"
                return infoMessage(mess)
        else:
            mess = "<h2>Пользователь с таким ником или email'ом уже существует"
            return infoMessage(mess)
    else:
        regForm = RegForm()
        return render(request, "auth.html", {"form" : regForm})

def users(request, name):
    return render(request, "home.html")
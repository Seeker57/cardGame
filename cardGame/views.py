from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Rarity, Card, Hero, HeroClass, CardClass, Player, CardPlayer, Deck, CardDeck
from .forms import AuthForm, RegForm, CreateDeck, EditDeck, AddCard
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


def createDeck(request, name):
    player = Player.objects.filter(nickname=name)
    if player:
        if request.method == "POST":
            newDeck = Deck()
            newDeck.name = request.POST.get("name")
            newDeck.player = player[0]
            deckHero = Hero.objects.filter(name=request.POST.get("hero"))
            if deckHero:
                newDeck.hero = deckHero[0]
            else:
                mess = "Героя {0} не существует".format(request.POST.get("hero"))
                return infoMessage(mess)
            newDeck.save()
            return HttpResponseRedirect("/users/" + name)
        else:
            createDeckForm = CreateDeck()
            heroes = player[0].heroplayer_set.all()
            return render(request, "createDeck.html", {"form": createDeckForm, "heroes" : heroes})
    else:
        return HttpResponse("<h2>Пользователь не найден</h2>")


def editDeck(request, name):
    player = Player.objects.filter(nickname=name)
    if player:
        if request.method == "POST":
            deckID = request.POST.get("deckID")
            deck = Deck.objects.filter(id=deckID)
            if deck:
                return HttpResponseRedirect("/users/" + name + '/editDeck/deck' + deckID)
            else:
                mess = "Колоды с id {0} не существует".format(deckID)
                return infoMessage(mess)
        else:
            editDeck = EditDeck()
            return render(request, "editDeck.html", {"form" : editDeck})
    else:
        return HttpResponse("<h2>Пользователь не найден</h2>")


def deleteDeck(request, name):
    player = Player.objects.filter(nickname=name)
    if player:
        if request.method == "POST":
            deckID = request.POST.get("deckID")
            deck = Deck.objects.filter(id=deckID)
            if deck:
                deck[0].delete()
                return HttpResponseRedirect("/users/" + name + '/decks')
            else:
                mess = "Колоды с id {0} не существует".format(deckID)
                return infoMessage(mess)
        else:
            editDeck = EditDeck()
            return render(request, "editDeck.html", {"form" : editDeck})
    else:
        return HttpResponse("<h2>Пользователь не найден</h2>")


def deck(request, name, deckID):
    player = Player.objects.filter(nickname=name)
    if player:
        if request.method == "POST":
            playerCards = player[0].cardplayer_set.all()
            chooseCard = playerCards.filter(card = request.POST.get("cardID"))
            if chooseCard:
                newCardDeck = CardDeck()
                newCardDeck.deck = Deck.objects.filter(id = int(deckID))[0]
                newCardDeck.card = chooseCard[0].card
                newCardDeck.save()
                return HttpResponseRedirect("/users/" + name + '/decks')
            else:
               mess = "Карты с id {0} у вас нет".format(request.POST.get("cardID"))
               return infoMessage(mess) 

        else:
            addCard = AddCard()
            cards = player[0].cardplayer_set.all()
            playerDeck = Deck.objects.filter(id = int(deckID))[0]
            classCards = []
            for card in cards:
                classes = card.card.cardclass_set.all()
                for class_f in classes:
                    if class_f.class_field == playerDeck.hero.class_field or \
                       class_f.class_field == HeroClass.objects.get(id=5):
                        classCards.append(card)
                        break
            return render(request, "chooseCard.html", {"form" : addCard, "cards" : classCards})
    else:
        return HttpResponse("<h2>Пользователь не найден</h2>")


def infoMessage(message):
    output = '<h2>' + message + '</h2>' +\
             '<form>' +\
             '<input type="button" value="Вернуться обратно" onclick="history.go(-2)">' +\
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
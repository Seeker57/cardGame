from django.db import models

# Create your models here.

class Card(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    mana = models.IntegerField()
    attack = models.IntegerField()
    hp = models.IntegerField()
    description = models.CharField(max_length=100, blank=True, null=True)
    art_path = models.CharField(max_length=50, blank=True, null=True)
    rarity = models.ForeignKey('Rarity', models.DO_NOTHING)


class CardClass(models.Model):
    card = models.ForeignKey(Card, models.DO_NOTHING)
    class_field = models.ForeignKey('HeroClass', models.DO_NOTHING, db_column='class_id')


class CardDeck(models.Model):
    card = models.ForeignKey(Card, models.DO_NOTHING)
    deck = models.ForeignKey('Deck', models.DO_NOTHING)


class CardMechanic(models.Model):
    card = models.ForeignKey(Card, models.DO_NOTHING)
    mechanic = models.ForeignKey('Mechanic', models.DO_NOTHING)


class CardPlayer(models.Model):
    card = models.ForeignKey(Card, models.DO_NOTHING)
    player = models.ForeignKey('Player', models.DO_NOTHING)


class CardType(models.Model):
    card = models.ForeignKey(Card, models.DO_NOTHING)
    type = models.ForeignKey('TypeCard', models.DO_NOTHING)


class Deck(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    hero = models.ForeignKey('Hero', models.DO_NOTHING)
    player = models.ForeignKey('Player', models.DO_NOTHING)


class Hero(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    hp = models.IntegerField()
    art_path = models.CharField(max_length=50, blank=True, null=True)
    class_field = models.ForeignKey('HeroClass', models.DO_NOTHING, db_column='class_id')
    power = models.ForeignKey('HeroPower', models.DO_NOTHING)


class HeroClass(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    feature = models.CharField(max_length=150, blank=True, null=True)


class HeroPower(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    mana = models.IntegerField()
    description = models.CharField(max_length=50, blank=True, null=True)


class Mechanic(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)


class Player(models.Model):
    nickname = models.CharField(unique=True, max_length=30, blank=True, null=True)
    login = models.CharField(unique=True, max_length=30, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    resourses = models.IntegerField()


class Rarity(models.Model):
    type_rarity = models.CharField(unique=True, max_length=15, blank=True, null=True)
    cost_create = models.IntegerField()
    cost_destruct = models.IntegerField()


class TypeCard(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)


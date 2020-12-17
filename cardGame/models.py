from django.db import models
from postgres_copy import CopyManager

# Create your models here.

class Card(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    mana = models.IntegerField()
    attack = models.IntegerField()
    hp = models.IntegerField()
    description = models.CharField(max_length=100, blank=True, null=True)
    art_path = models.CharField(max_length=50, blank=True, null=True)
    rarity = models.ForeignKey('Rarity', models.RESTRICT)
    objects = CopyManager()


class CardClass(models.Model):
    card = models.ForeignKey(Card, models.RESTRICT)
    class_field = models.ForeignKey('HeroClass', models.RESTRICT, db_column='class_id')
    objects = CopyManager()


class CardDeck(models.Model):
    card = models.ForeignKey(Card, models.CASCADE)
    deck = models.ForeignKey('Deck', models.CASCADE)
    objects = CopyManager()


class CardMechanic(models.Model):
    card = models.ForeignKey(Card, models.RESTRICT)
    mechanic = models.ForeignKey('Mechanic', models.RESTRICT)
    objects = CopyManager()


class CardPlayer(models.Model):
    card = models.ForeignKey(Card, models.CASCADE)
    player = models.ForeignKey('Player', models.CASCADE)
    objects = CopyManager()


class CardType(models.Model):
    card = models.ForeignKey(Card, models.RESTRICT)
    type = models.ForeignKey('TypeCard', models.RESTRICT)
    objects = CopyManager()


class Deck(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    hero = models.ForeignKey('Hero', models.CASCADE)
    player = models.ForeignKey('Player', models.CASCADE)
    objects = CopyManager()


class Hero(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    hp = models.IntegerField()
    art_path = models.CharField(max_length=50, blank=True, null=True)
    class_field = models.ForeignKey('HeroClass', models.RESTRICT, db_column='class_id')
    power = models.ForeignKey('HeroPower', models.RESTRICT)
    objects = CopyManager()


class HeroClass(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    feature = models.CharField(max_length=150, blank=True, null=True)
    objects = CopyManager()


class HeroPower(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    mana = models.IntegerField()
    description = models.CharField(max_length=50, blank=True, null=True)
    objects = CopyManager()


class Mechanic(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    objects = CopyManager()


class Player(models.Model):
    nickname = models.CharField(unique=True, max_length=30, blank=True, null=True)
    login = models.CharField(unique=True, max_length=30, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    resourses = models.IntegerField()
    objects = CopyManager()


class Rarity(models.Model):
    type_rarity = models.CharField(unique=True, max_length=15, blank=True, null=True)
    cost_create = models.IntegerField()
    cost_destruct = models.IntegerField()
    objects = CopyManager()


class TypeCard(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    objects = CopyManager()


class HeroPlayer(models.Model):
    hero = models.ForeignKey(Hero, models.CASCADE)
    player = models.ForeignKey(Player, models.CASCADE)
    objects = CopyManager()
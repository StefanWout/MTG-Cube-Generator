from django.db import models
from django.contrib.auth.models import User


class Archetype(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500)
    # Assuming it holds concatenated color values (e.g., "WUBRG")
    color_identities = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Card(models.Model):
    COLOR_CHOICES = [
        ('W', 'White'),
        ('U', 'Blue'),
        ('B', 'Black'),
        ('R', 'Red'),
        ('G', 'Green'),
        ('C', 'Colorless'),

        # Two-Color Combinations
        ('WU', 'White-Blue'),
        ('WB', 'White-Black'),
        ('WR', 'White-Red'),
        ('WG', 'White-Green'),
        ('UB', 'Blue-Black'),
        ('UR', 'Blue-Red'),
        ('UG', 'Blue-Green'),
        ('BR', 'Black-Red'),
        ('BG', 'Black-Green'),
        ('RG', 'Red-Green'),

        # Three-Color Combinations
        ('WUB', 'White-Blue-Black'),
        ('WUR', 'White-Blue-Red'),
        ('WUG', 'White-Blue-Green'),
        ('WBR', 'White-Black-Red'),
        ('WBG', 'White-Black-Green'),
        ('WRG', 'White-Red-Green'),
        ('UBR', 'Blue-Black-Red'),
        ('UBG', 'Blue-Black-Green'),
        ('URG', 'Blue-Red-Green'),
        ('BRG', 'Black-Red-Green'),

        # Four-Color Combinations
        ('WUBR', 'White-Blue-Black-Red'),
        ('WUBG', 'White-Blue-Black-Green'),
        ('WURG', 'White-Blue-Red-Green'),
        ('WBRG', 'White-Black-Red-Green'),
        ('UBRG', 'Blue-Black-Red-Green'),

        # Five-Color Combination
        ('WUBRG', 'White-Blue-Black-Red-Green')
    ]
    scryfall_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mana_cost = models.CharField(max_length=50, blank=True, null=True)
    mana_value = models.DecimalField(max_digits=10, decimal_places=2)
    type_line = models.CharField(max_length=255)
    oracle_text = models.CharField(max_length=1000, blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    toughness = models.IntegerField(blank=True, null=True)
    color_identity = models.CharField(max_length=10, choices=COLOR_CHOICES)
    set_name = models.CharField(max_length=255)
    rarity = models.CharField(max_length=50)
    edhrec_rank = models.IntegerField()
    archetypes = models.ManyToManyField(Archetype)
    img_url = models.URLField()

    def __str__(self):
        return self.name


class Cube(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    cards = models.ManyToManyField(Card)
    archetypes = models.ManyToManyField(Archetype)
    color_identities = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

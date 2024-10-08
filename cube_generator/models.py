from django.db import models
from django.contrib.auth.models import User

class Archetype(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500)
    possible_colors = models.ManyToManyField(
        'ColorIdentity',
        related_name='archetypes',
    )
    
    # Add fields to store archetype-specific analysis criteria
    keywords = models.JSONField(
        default=list,
        help_text="List of keywords associated with this archetype"
    )
    oracle_patterns = models.JSONField(
        default=list,
        help_text="List of regex patterns to match in oracle text"
    )

    def __str__(self):
        return self.name


class Card(models.Model):
    scryfall_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    mana_cost = models.CharField(max_length=50, blank=True, null=True)
    mana_value = models.DecimalField(max_digits=10, decimal_places=2)
    type_line = models.CharField(max_length=255)
    oracle_text = models.CharField(max_length=1000, blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    toughness = models.IntegerField(blank=True, null=True)
    color_identity = models.CharField(
        max_length=10, 
        choices=ColorIdentity.COLOR_CHOICES
    )
    set_name = models.CharField(max_length=255)
    rarity = models.CharField(max_length=50)
    edhrec_rank = models.IntegerField()
    img_url = models.URLField()
    
    # Store archetype weights as a JSON object
    archetype_weights = models.JSONField(
        default=dict,
        help_text="Maps archetype IDs to weights: {'Aristocrat': 8, 'Spellslinger': 6}"
    )
    
    # Add an index specifically for EDHREC ranking to help with filtering
    class Meta:
        indexes = [
            models.Index(fields=['edhrec_rank']),
        ]

    def get_archetype_weight(self, archetype_id):
        """Get the weight for a specific archetype"""
        return self.archetype_weights.get(str(archetype_id), 0)
    
    def set_archetype_weight(self, archetype_id, weight):
        """Set the weight for a specific archetype"""
        if weight > 0:  # Only store non-zero weights
            self.archetype_weights[str(archetype_id)] = weight
        elif str(archetype_id) in self.archetype_weights:
            del self.archetype_weights[str(archetype_id)]
    
    @property
    def primary_archetypes(self):
        """Return archetypes with weight >= 7"""
        return [aid for aid, weight in self.archetype_weights.items() 
               if weight >= 7]
    
    def __str__(self):
        return self.name

class ColorIdentity(models.Model):
    """Represents possible color combinations in Magic, ordered alphabetically per Scryfall"""
    COLOR_CHOICES = [
        ('W', 'White'),
        ('U', 'Blue'),
        ('B', 'Black'),
        ('R', 'Red'),
        ('G', 'Green'),
        ('C', 'Colorless'),
        # Two-Color Combinations
        ('UW', 'White-Blue'),
        ('BW', 'White-Black'),
        ('RW', 'White-Red'),
        ('GW', 'White-Green'),
        ('BU', 'Blue-Black'),
        ('RU', 'Blue-Red'),
        ('GU', 'Blue-Green'),
        ('BR', 'Black-Red'),
        ('BG', 'Black-Green'),
        ('GR', 'Red-Green'),
        # Three-Color Combinations
        ('BUW', 'White-Blue-Black'),
        ('RUW', 'White-Blue-Red'),
        ('GUW', 'White-Blue-Green'),
        ('BRW', 'White-Black-Red'),
        ('BGW', 'White-Black-Green'),
        ('GRW', 'White-Red-Green'),
        ('BRU', 'Blue-Black-Red'),
        ('BGU', 'Blue-Black-Green'),
        ('GRU', 'Blue-Red-Green'),
        ('BGR', 'Black-Red-Green'),
        # Four-Color Combinations
        ('BRUW', 'White-Blue-Black-Red'),
        ('BGUW', 'White-Blue-Black-Green'),
        ('GRUW', 'White-Blue-Red-Green'),
        ('BGRW', 'White-Black-Red-Green'),
        ('BGRU', 'Blue-Black-Red-Green'),
        # Five-Color Combination
        ('BGRUW', 'White-Blue-Black-Red-Green')
    ]
    
    colors = models.CharField(max_length=10, choices=COLOR_CHOICES, unique=True)
    
    def __str__(self):
        return dict(self.COLOR_CHOICES)[self.colors]
    
    class Meta:
        verbose_name_plural = "Color Identities"

class Cube(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    cards = models.ManyToManyField(Card)
    archetypes = models.ManyToManyField(Archetype)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
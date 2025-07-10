
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


class GameSession(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255)
    strength = models.PositiveIntegerField(default=10)
    dexterity = models.PositiveIntegerField(default=10)
    constitution = models.PositiveIntegerField(default=10)
    intelligence = models.PositiveIntegerField(default=10)
    wisdom = models.PositiveIntegerField(default=10)
    charisma = models.PositiveIntegerField(default=10)
    armor_class = models.PositiveIntegerField(default=10)
    max_hp = models.PositiveIntegerField(default=10)

    size = models.CharField(max_length=50, blank=True, null=True)
    creature_type = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    damage_immunities = models.TextField(blank=True, null=True)
    condition_immunities = models.TextField(blank=True, null=True)
    senses = models.TextField(blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    challenge_rating = models.CharField(max_length=50, blank=True, null=True)
    actions_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    race = models.CharField(max_length=100, blank=True, null=True)
    proficiency_bonus = models.PositiveIntegerField(default=2)
    speed = models.CharField(max_length=50, blank=True, null=True)

    traits_description = models.TextField(blank=True, null=True)
    proficiencies_description = models.TextField(blank=True, null=True)
    equipment_description = models.TextField(blank=True, null=True)
    attacks_description = models.TextField(blank=True, null=True)
    coins_description = models.TextField(blank=True, null=True)
    resources_description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Hero(Character):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='heroes')
    current_hp = models.IntegerField()
    player_name = models.CharField(max_length=255, blank=True, null=True)

    char_class = models.CharField(max_length=100, blank=True, null=True)
    char_subclass = models.CharField(max_length=100, blank=True, null=True)
    level = models.PositiveIntegerField(default=1)
    background = models.CharField(max_length=100, blank=True, null=True)
    alignment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Enemy(Character):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='enemies')

    def __str__(self):
        return self.name


class Encounter(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='encounters')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    current_round = models.PositiveIntegerField(default=0)
    active_combatant_index = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Combatant(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='combatants')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    character = GenericForeignKey('content_type', 'object_id')
    current_hp = models.IntegerField()
    initiative = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.character} in {self.encounter.name}'

    def clean(self):
        if self.current_hp < 0:
            raise ValidationError({'current_hp': 'HP cannot be negative.'})


class EncounterLog(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='logs')
    actor = models.ForeignKey(Combatant, on_delete=models.CASCADE, related_name='actions', null=True, blank=True)
    target = models.ForeignKey(Combatant, on_delete=models.CASCADE, related_name='targeted_actions', null=True, blank=True)
    action_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_at}: {self.action_description}'

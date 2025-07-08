from django.db import models


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

    # Monster-specific fields (now directly in Character)
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

    # General fields (race remains here as it applies to both heroes and some enemies)
    race = models.CharField(max_length=100, blank=True, null=True)
    proficiency_bonus = models.PositiveIntegerField(default=2)
    speed = models.CharField(max_length=50, blank=True, null=True)

    # Text fields for complex data (already existing)
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

    # Fields moved from Character to Hero
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
    # New fields for turn/round tracking
    current_round = models.PositiveIntegerField(default=0)
    active_combatant_index = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Combatant(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='combatants')
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, null=True, blank=True)
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE, null=True, blank=True)
    current_hp = models.IntegerField()
    initiative = models.PositiveIntegerField()

    def __str__(self):
        if self.hero:
            return f'{self.hero.name} in {self.encounter.name}'
        elif self.enemy:
            return f'{self.enemy.name} in {self.encounter.name}'
        return f'Combatant in {self.encounter.name}'


class EncounterLog(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='logs')
    actor = models.ForeignKey(Combatant, on_delete=models.CASCADE, related_name='actions', null=True, blank=True)
    target = models.ForeignKey(Combatant, on_delete=models.CASCADE, related_name='targeted_actions', null=True, blank=True)
    action_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_at}: {self.action_description}'
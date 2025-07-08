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

    class Meta:
        abstract = True


class Hero(Character):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='heroes')
    current_hp = models.IntegerField()

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

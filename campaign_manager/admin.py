from django.contrib import admin
from .models import GameSession, Hero, Enemy, Encounter, Combatant, EncounterLog


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_session', 'max_hp', 'armor_class')


@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_session', 'max_hp', 'armor_class')


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_session', 'is_active', 'created_at')


@admin.register(Combatant)
class CombatantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'current_hp', 'initiative')


@admin.register(EncounterLog)
class EncounterLogAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
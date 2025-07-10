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
    list_display = ('encounter', 'character_display', 'current_hp', 'initiative')
    search_fields = ('encounter__name',)
    list_filter = ('encounter__game_session',)

    def character_display(self, obj):
        return f"{obj.character} ({obj.content_type})"
    character_display.short_description = 'Character'

@admin.register(EncounterLog)
class EncounterLogAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

from django.shortcuts import render, get_object_or_404, redirect
import random
from .models import GameSession, Hero, Enemy, Encounter, Combatant, EncounterLog
from .forms import HeroForm, EnemyForm, EncounterForm, AttackForm, HealForm

def heal(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    if request.method == 'POST':
        form = HealForm(request.POST, encounter=encounter)
        if form.is_valid():
            healer = form.cleaned_data['healer']
            target = form.cleaned_data['target']
            amount = form.cleaned_data['amount']

            target.current_hp = min(target.current_hp + amount, target.hero.max_hp if target.hero else target.enemy.max_hp)
            target.save()

            if target.hero:
                target.hero.current_hp = target.current_hp
                target.hero.save()

            EncounterLog.objects.create(
                encounter=encounter,
                actor=healer,
                target=target,
                action_description=f'{healer} heals {target} for {amount} HP.'
            )
            return redirect('encounter_detail', pk=encounter.pk)
    return redirect('encounter_detail', pk=encounter.pk)

def game_session_list(request):
    sessions = GameSession.objects.all()
    return render(request, 'campaign_manager/game_session_list.html', {'sessions': sessions})

def game_session_detail(request, pk):
    session = get_object_or_404(GameSession, pk=pk)
    return render(request, 'campaign_manager/game_session_detail.html', {'session': session})

# Hero CRUD
def hero_list(request, game_session_pk):
    game_session = get_object_or_404(GameSession, pk=game_session_pk)
    heroes = Hero.objects.filter(game_session=game_session)
    return render(request, 'campaign_manager/hero_list.html', {'game_session': game_session, 'heroes': heroes})

def hero_create(request, game_session_pk):
    game_session = get_object_or_404(GameSession, pk=game_session_pk)
    if request.method == 'POST':
        form = HeroForm(request.POST)
        if form.is_valid():
            hero = form.save(commit=False)
            hero.game_session = game_session
            hero.current_hp = hero.max_hp  # Set current_hp to max_hp on creation
            hero.save()
            return redirect('hero_list', game_session_pk=game_session.pk)
    else:
        form = HeroForm(initial={'game_session': game_session})
    return render(request, 'campaign_manager/hero_form.html', {'form': form, 'game_session': game_session})

def hero_update(request, pk):
    hero = get_object_or_404(Hero, pk=pk)
    if request.method == 'POST':
        form = HeroForm(request.POST, instance=hero)
        if form.is_valid():
            form.save()
            return redirect('hero_list', game_session_pk=hero.game_session.pk)
    else:
        form = HeroForm(instance=hero)
    return render(request, 'campaign_manager/hero_form.html', {'form': form, 'game_session': hero.game_session})

def hero_delete(request, pk):
    hero = get_object_or_404(Hero, pk=pk)
    game_session_pk = hero.game_session.pk
    if request.method == 'POST':
        hero.delete()
        return redirect('hero_list', game_session_pk=game_session_pk)
    return render(request, 'campaign_manager/hero_confirm_delete.html', {'hero': hero})

# Enemy CRUD
def enemy_list(request, game_session_pk):
    game_session = get_object_or_404(GameSession, pk=game_session_pk)
    enemies = Enemy.objects.filter(game_session=game_session)
    return render(request, 'campaign_manager/enemy_list.html', {'game_session': game_session, 'enemies': enemies})

def enemy_create(request, game_session_pk):
    game_session = get_object_or_404(GameSession, pk=game_session_pk)
    if request.method == 'POST':
        form = EnemyForm(request.POST)
        if form.is_valid():
            enemy = form.save(commit=False)
            enemy.game_session = game_session
            enemy.save()
            return redirect('enemy_list', game_session_pk=game_session.pk)
    else:
        form = EnemyForm(initial={'game_session': game_session})
    return render(request, 'campaign_manager/enemy_form.html', {'form': form, 'game_session': game_session})

def enemy_update(request, pk):
    enemy = get_object_or_404(Enemy, pk=pk)
    if request.method == 'POST':
        form = EnemyForm(request.POST, instance=enemy)
        if form.is_valid():
            form.save()
            return redirect('enemy_list', game_session_pk=enemy.game_session.pk)
    else:
        form = EnemyForm(instance=enemy)
    return render(request, 'campaign_manager/enemy_form.html', {'form': form, 'game_session': enemy.game_session})

def enemy_delete(request, pk):
    enemy = get_object_or_404(Enemy, pk=pk)
    game_session_pk = enemy.game_session.pk
    if request.method == 'POST':
        enemy.delete()
        return redirect('enemy_list', game_session_pk=game_session_pk)
    return render(request, 'campaign_manager/enemy_confirm_delete.html', {'enemy': enemy})

# Encounter CRUD
def encounter_list(request, game_session_pk):
    game_session = get_object_or_404(GameSession, pk=game_session_pk)
    encounters = Encounter.objects.filter(game_session=game_session)
    return render(request, 'campaign_manager/encounter_list.html', {'game_session': game_session, 'encounters': encounters})

def encounter_create(request, game_session_pk):
    game_session = get_object_or_404(GameSession, pk=game_session_pk)
    if request.method == 'POST':
        form = EncounterForm(request.POST)
        if form.is_valid():
            encounter = form.save(commit=False)
            encounter.game_session = game_session
            encounter.save()
            return redirect('game_session_detail', pk=game_session.pk)
    else:
        form = EncounterForm(initial={'game_session': game_session})
    return render(request, 'campaign_manager/encounter_form.html', {'form': form, 'game_session': game_session})

def encounter_update(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    if request.method == 'POST':
        form = EncounterForm(request.POST, instance=encounter)
        if form.is_valid():
            form.save()
            return redirect('encounter_list', game_session_pk=encounter.game_session.pk)
    else:
        form = EncounterForm(instance=encounter)
    return render(request, 'campaign_manager/encounter_form.html', {'form': form, 'game_session': encounter.game_session})

def encounter_delete(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    game_session_pk = encounter.game_session.pk
    if request.method == 'POST':
        encounter.delete()
        return redirect('game_session_detail', pk=game_session_pk)
    return render(request, 'campaign_manager/encounter_confirm_delete.html', {'encounter': encounter})

def encounter_detail(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    attack_form = AttackForm(encounter=encounter)
    combatants = encounter.combatants.order_by('-initiative')
    return render(request, 'campaign_manager/encounter_detail.html', {'encounter': encounter, 'attack_form': attack_form, 'combatants': combatants})

def start_encounter(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    if request.method == 'POST':
        # Clear existing combatants and logs
        encounter.combatants.all().delete()
        encounter.logs.all().delete()

        # Reset encounter state
        encounter.current_round = 1
        encounter.active_combatant_index = 0
        encounter.save()

        # Add heroes
        for hero in encounter.game_session.heroes.all():
            initiative = random.randint(1, 20) + ((hero.dexterity - 10) // 2)
            Combatant.objects.create(encounter=encounter, hero=hero, current_hp=hero.current_hp, initiative=initiative)

        # Add enemies based on quantities
        for enemy in encounter.game_session.enemies.all():
            quantity_key = f'enemy_quantities_{enemy.pk}'
            quantity = int(request.POST.get(quantity_key, 0))
            for _ in range(quantity):
                initiative = random.randint(1, 20) + ((enemy.dexterity - 10) // 2)
                Combatant.objects.create(encounter=encounter, enemy=enemy, current_hp=enemy.max_hp, initiative=initiative)
        
        EncounterLog.objects.create(encounter=encounter, action_description=f"Round 1 begins!")

        return redirect('encounter_detail', pk=encounter.pk)
    return redirect('encounter_detail', pk=encounter.pk)


def next_turn(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    if request.method == 'POST':
        combatants = list(encounter.combatants.order_by('-initiative'))
        
        if not combatants:
            return redirect('encounter_detail', pk=encounter.pk)

        # Move to the next combatant
        encounter.active_combatant_index += 1

        # Loop to find the next active combatant, skipping defeated ones
        while True:
            if encounter.active_combatant_index >= len(combatants):
                encounter.active_combatant_index = 0
                encounter.current_round += 1
                EncounterLog.objects.create(encounter=encounter, action_description=f"Round {encounter.current_round} begins!")
            
            # Check if the current combatant is alive
            if combatants[encounter.active_combatant_index].current_hp > 0:
                break # Found an active combatant
            else:
                # If defeated, move to the next one immediately
                encounter.active_combatant_index += 1

        # Check for end of encounter
        heroes_alive = any(c.hero and c.current_hp > 0 for c in combatants)
        enemies_alive = any(c.enemy and c.current_hp > 0 for c in combatants)

        if not heroes_alive or not enemies_alive:
            encounter.is_active = False
            EncounterLog.objects.create(encounter=encounter, action_description="Encounter ended!")
            encounter.save()
            return redirect('game_session_detail', pk=encounter.game_session.pk)

        encounter.save()
    return redirect('encounter_detail', pk=encounter.pk)

def attack(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    if request.method == 'POST':
        form = AttackForm(request.POST, encounter=encounter)
        if form.is_valid():
            attacker = form.cleaned_data['attacker']
            target = form.cleaned_data['target']
            damage = form.cleaned_data['damage']

            target.current_hp -= damage
            target.save()

            if target.hero:
                target.hero.current_hp = target.current_hp
                target.hero.save()

            EncounterLog.objects.create(
                encounter=encounter,
                actor=attacker,
                target=target,
                action_description=f'{attacker} attacks {target} for {damage} damage.'
            )

            if target.current_hp <= 0:
                EncounterLog.objects.create(
                    encounter=encounter,
                    target=target,
                    action_description=f'{target} has been defeated!'
                )
            return redirect('encounter_detail', pk=encounter.pk)
    return redirect('encounter_detail', pk=encounter.pk)

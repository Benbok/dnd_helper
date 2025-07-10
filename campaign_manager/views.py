from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _t
from django.http import JsonResponse
import random
from .models import GameSession, Hero, Enemy, Encounter, Combatant, EncounterLog
from .forms import HeroForm, EnemyForm, EncounterForm, AttackForm, HealForm
from django.contrib import messages


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


def hero_detail(request, pk):
    hero = get_object_or_404(Hero, pk=pk)
    return render(request, 'campaign_manager/hero_detail.html', {'hero': hero})


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


def enemy_detail(request, pk):
    enemy = get_object_or_404(Enemy, pk=pk)
    return render(request, 'campaign_manager/enemy_detail.html', {'enemy': enemy})


# Encounter CRUD
def encounter_list(request, game_session_pk):
    game_session = get_object_or_404(GameSession, pk=game_session_pk)
    encounters = Encounter.objects.filter(game_session=game_session)
    return render(request, 'campaign_manager/encounter_list.html',
                  {'game_session': game_session, 'encounters': encounters})


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
    return render(request, 'campaign_manager/encounter_form.html',
                  {'form': form, 'game_session': encounter.game_session})


def encounter_delete(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    game_session_pk = encounter.game_session.pk
    if request.method == 'POST':
        encounter.delete()
        return redirect('game_session_detail', pk=game_session_pk)
    return render(request, 'campaign_manager/encounter_confirm_delete.html', {'encounter': encounter})


from django.contrib.contenttypes.models import ContentType
from .models import Hero

def encounter_detail(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    attack_form = AttackForm(encounter=encounter)

    hero_type = ContentType.objects.get_for_model(Hero)
    enemy_type = ContentType.objects.get_for_model(Enemy)

    combatants_queryset = encounter.combatants.order_by('-initiative')
    combatants_data = []
    heroes = []
    enemies = []

    for c in combatants_queryset:
        try:
            character_obj = c.character
            is_hero = c.content_type == hero_type
            combatant_info = {
                'id': c.pk,
                'name': character_obj.name,
                'current_hp': c.current_hp,
                'max_hp': character_obj.max_hp,
                'initiative': c.initiative,
                'is_hero': is_hero,
                'strength': character_obj.strength,
                'strength_modifier': (character_obj.strength - 10) // 2,
                'dexterity': character_obj.dexterity,
                'dexterity_modifier': (character_obj.dexterity - 10) // 2,
                'constitution': character_obj.constitution,
                'constitution_modifier': (character_obj.constitution - 10) // 2,
                'intelligence': character_obj.intelligence,
                'intelligence_modifier': (character_obj.intelligence - 10) // 2,
                'wisdom': character_obj.wisdom,
                'wisdom_modifier': (character_obj.wisdom - 10) // 2,
                'charisma': character_obj.charisma,
                'charisma_modifier': (character_obj.charisma - 10) // 2,
                'armor_class': character_obj.armor_class,
            }
            combatants_data.append(combatant_info)
            if is_hero:
                heroes.append(combatant_info)
            else:
                enemies.append(combatant_info)
        except Exception as e:
            print(f"Combatant id={c.pk}, content_type={c.content_type}, object_id={c.object_id}: {e}")
            continue

    return render(request, 'campaign_manager/encounter_detail.html', {
        'encounter': encounter,
        'attack_form': attack_form,
        'combatants': combatants_data,
        'heroes': heroes,
        'enemies': enemies,
    })



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
        hero_type = ContentType.objects.get_for_model(Hero)
        enemy_type = ContentType.objects.get_for_model(Enemy)

        # Для героев:
        for hero in encounter.game_session.heroes.all():
            initiative = random.randint(1, 20) + ((hero.dexterity - 10) // 2)
            Combatant.objects.create(
                encounter=encounter,
                content_type=hero_type,
                object_id=hero.pk,
                current_hp=hero.current_hp,
                initiative=initiative
            )

        # Для врагов:
        for enemy in encounter.game_session.enemies.all():
            quantity_key = f'enemy_quantities_{enemy.pk}'
            quantity = int(request.POST.get(quantity_key, 0))
            for _ in range(quantity):
                initiative = random.randint(1, 20) + ((enemy.dexterity - 10) // 2)
                Combatant.objects.create(
                    encounter=encounter,
                    content_type=enemy_type,
                    object_id=enemy.pk,
                    current_hp=enemy.max_hp,
                    initiative=initiative
                )

        EncounterLog.objects.create(encounter=encounter, action_description=_t("Round 1 begins!"))

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
                EncounterLog.objects.create(encounter=encounter,
                                            action_description=_t("Round %(round_num)s begins!") % {
                                                'round_num': encounter.current_round})

            # Check if the current combatant is alive
            if combatants[encounter.active_combatant_index].current_hp > 0:
                break  # Found an active combatant
            else:
                # If defeated, move to the next one immediately
                encounter.active_combatant_index += 1

        # Check for end of encounter
        hero_type = ContentType.objects.get_for_model(Hero)
        enemy_type = ContentType.objects.get_for_model(Enemy)

        heroes_alive = any(c.content_type == hero_type and c.current_hp > 0 for c in combatants)
        enemies_alive = any(c.content_type == enemy_type and c.current_hp > 0 for c in combatants)

        if not heroes_alive or not enemies_alive:
            encounter.is_active = False
            EncounterLog.objects.create(encounter=encounter, action_description=_t("Encounter ended!"))
            encounter.save()
            return redirect('game_session_detail', pk=encounter.game_session.pk)

        encounter.save()
    return redirect('encounter_detail', pk=encounter.pk)


from django.contrib.contenttypes.models import ContentType
from .models import Hero  # Импорт Hero для проверки типа

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

            # Если это герой — обновить его HP
            hero_type = ContentType.objects.get_for_model(Hero)
            if target.content_type == hero_type:
                target.character.current_hp = target.current_hp
                target.character.save()

            EncounterLog.objects.create(
                encounter=encounter,
                actor=attacker,
                target=target,
                action_description=_t('%(attacker)s attacks %(target)s for %(damage)s damage.') % {
                    'attacker': attacker.character.name,
                    'target': target.character.name,
                    'damage': damage
                }
            )

            if target.current_hp <= 0:
                EncounterLog.objects.create(
                    encounter=encounter,
                    target=target,
                    action_description=_t('%(target)s has been defeated!') % {'target': target.character.name}
                )

            messages.success(request, _t("Attack successful!"))
        else:
            messages.error(request, _t("Invalid form data."))

    return redirect('encounter_detail', pk=encounter.pk)



def heal(request, pk):
    encounter = get_object_or_404(Encounter, pk=pk)
    if request.method == 'POST':
        form = HealForm(request.POST, encounter=encounter)
        if form.is_valid():
            healer = form.cleaned_data['healer']
            target = form.cleaned_data['target']
            amount = form.cleaned_data['amount']

            target.current_hp = min(target.current_hp + amount,
                                    target.character.max_hp)
            target.save()

            if hasattr(target.character, 'current_hp'):
                target.character.current_hp = target.current_hp
                target.character.save()

            EncounterLog.objects.create(
                encounter=encounter,
                actor=healer,
                target=target,
                action_description=_t('%(healer)s heals %(target)s for %(amount)s HP.') % {
                    'healer': healer.character.name,
                    'target': target.character.name,
                    'amount': amount
                }
            )

            messages.success(request, _t("Healing successful!"))
        else:
            messages.error(request, _t("Invalid form data."))

    return redirect('encounter_detail', pk=encounter.pk)


def roll_ability_check(request, encounter_id, character_id, character_type, ability_name):
    encounter = get_object_or_404(Encounter, pk=encounter_id)

    if character_type == 'hero':
        character = get_object_or_404(Hero, pk=character_id)
    elif character_type == 'enemy':
        character = get_object_or_404(Enemy, pk=character_id)
    else:
        return JsonResponse({'error': _t("Invalid character type.")}, status=400)

    ability_score = getattr(character, ability_name.lower(), None)
    if ability_score is None:
        return JsonResponse({'error': _t("Invalid ability name.")}, status=400)

    roll = random.randint(1, 20)
    modifier = (ability_score - 10) // 2
    result = roll + modifier

    character_name = character.name

    message = _t("%(character_name)s rolls %(roll)s + %(modifier)s (%(ability_name)s) = %(result)s") % {
        'character_name': character_name,
        'roll': roll,
        'modifier': modifier,
        'ability_name': ability_name,
        'result': result
    }

    # Log to EncounterLog
    EncounterLog.objects.create(
        encounter=encounter,
        action_description=message
    )
    hero_type = ContentType.objects.get_for_model(Hero)
    # Fetch updated logs and combatants for AJAX response
    logs = list(encounter.logs.values('action_description'))
    combatants_data = []
    for c in encounter.combatants.order_by('-initiative'):
        character_obj = c.character
        combatants_data.append({
            'id': c.pk,
            'name': character_obj.name,
            'current_hp': c.current_hp,
            'max_hp': character_obj.max_hp,
            'initiative': c.initiative,
            'is_hero': c.content_type == hero_type,
            'strength': character_obj.strength,
            'strength_modifier': (character_obj.strength - 10) // 2,
            'dexterity': character_obj.dexterity,
            'dexterity_modifier': (character_obj.dexterity - 10) // 2,
            'constitution': character_obj.constitution,
            'constitution_modifier': (character_obj.constitution - 10) // 2,
            'intelligence': character_obj.intelligence,
            'intelligence_modifier': (character_obj.intelligence - 10) // 2,
            'wisdom': character_obj.wisdom,
            'wisdom_modifier': (character_obj.wisdom - 10) // 2,
            'charisma': character_obj.charisma,
            'charisma_modifier': (character_obj.charisma - 10) // 2,
            'armor_class': character_obj.armor_class,
        })
    return JsonResponse({'message': message, 'logs': logs, 'combatants': combatants_data})


def roll_general_ability_check(request, character_id, character_type, ability_name):
    if character_type == 'hero':
        character = get_object_or_404(Hero, pk=character_id)
    elif character_type == 'enemy':
        character = get_object_or_404(Enemy, pk=character_id)
    else:
        return JsonResponse({'error': _t("Invalid character type.")}, status=400)

    ability_score = getattr(character, ability_name.lower(), None)
    if ability_score is None:
        return JsonResponse({'error': _t("Invalid ability name.")}, status=400)

    roll = random.randint(1, 20)
    modifier = (ability_score - 10) // 2
    result = roll + modifier

    character_name = character.name

    message = _t("%(character_name)s rolls %(roll)s + %(modifier)s (%(ability_name)s) = %(result)s") % {
        'character_name': character_name,
        'roll': roll,
        'modifier': modifier,
        'ability_name': ability_name,
        'result': result
    }

    return JsonResponse({'message': message})
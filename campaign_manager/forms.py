from django import forms
from .models import Hero, Enemy, Encounter, Combatant

RACE_CHOICES = [
    ('Дварф', 'Дварф'),
    ('Полурослик', 'Полурослик'),
    ('Человек', 'Человек'),
    ('Эльф', 'Эльф'),
    ('Гном', 'Гном'),
    ('Драконорожденный', 'Драконорожденный'),
    ('Полуорк', 'Полуорк'),
    ('Полуэльф', 'Полуэльф'),
    ('Тифлинг', 'Тифлинг'),
]

CLASS_CHOICES = [
    ('Бард', 'Бард'),
    ('Варвар', 'Варвар'),
    ('Воин', 'Воин'),
    ('Волшебник', 'Волшебник'),
    ('Друид', 'Друид'),
    ('Жрец', 'Жрец'),
    ('Колдун', 'Колдун'),
    ('Монах', 'Монах'),
    ('Паладин', 'Паладин'),
    ('Плут', 'Плут'),
    ('Следопыт', 'Следопыт'),
    ('Чародей', 'Чародей'),
]

class HeroForm(forms.ModelForm):
    race = forms.ChoiceField(choices=RACE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    char_class = forms.ChoiceField(choices=CLASS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Hero
        exclude = ('current_hp', 'game_session',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'player_name': forms.TextInput(attrs={'class': 'form-control'}),
            'char_subclass': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.NumberInput(attrs={'class': 'form-control'}),
            'background': forms.TextInput(attrs={'class': 'form-control'}),
            'alignment': forms.TextInput(attrs={'class': 'form-control'}),
            'proficiency_bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'speed': forms.TextInput(attrs={'class': 'form-control'}),
            'strength': forms.NumberInput(attrs={'class': 'form-control'}),
            'dexterity': forms.NumberInput(attrs={'class': 'form-control'}),
            'constitution': forms.NumberInput(attrs={'class': 'form-control'}),
            'intelligence': forms.NumberInput(attrs={'class': 'form-control'}),
            'wisdom': forms.NumberInput(attrs={'class': 'form-control'}),
            'charisma': forms.NumberInput(attrs={'class': 'form-control'}),
            'armor_class': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_hp': forms.NumberInput(attrs={'class': 'form-control'}),
            'traits_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proficiencies_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'equipment_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attacks_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'coins_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resources_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'game_session': forms.HiddenInput(),
        }

class EnemyForm(forms.ModelForm):
    class Meta:
        model = Enemy
        exclude = (
            'game_session', 'char_class', 'char_subclass', 'background', 'alignment', 'race'
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.NumberInput(attrs={'class': 'form-control'}),
            'proficiency_bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'speed': forms.TextInput(attrs={'class': 'form-control'}),
            'strength': forms.NumberInput(attrs={'class': 'form-control'}),
            'dexterity': forms.NumberInput(attrs={'class': 'form-control'}),
            'constitution': forms.NumberInput(attrs={'class': 'form-control'}),
            'intelligence': forms.NumberInput(attrs={'class': 'form-control'}),
            'wisdom': forms.NumberInput(attrs={'class': 'form-control'}),
            'charisma': forms.NumberInput(attrs={'class': 'form-control'}),
            'armor_class': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_hp': forms.NumberInput(attrs={'class': 'form-control'}),
            'traits_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proficiencies_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'equipment_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attacks_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'coins_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resources_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'creature_type': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'damage_immunities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'condition_immunities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'senses': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'languages': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'challenge_rating': forms.TextInput(attrs={'class': 'form-control'}),
            'actions_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'game_session': forms.HiddenInput(),
        }

class EncounterForm(forms.ModelForm):
    class Meta:
        model = Encounter
        fields = ['name', 'description', 'game_session']
        widgets = {
            'game_session': forms.HiddenInput(),
        }

class AttackForm(forms.Form):
    attacker = forms.ModelChoiceField(queryset=Combatant.objects.all(), widget=forms.HiddenInput())
    target = forms.ModelChoiceField(queryset=Combatant.objects.all())
    damage = forms.IntegerField(min_value=0)

    def __init__(self, *args, **kwargs):
        encounter = kwargs.pop('encounter', None)
        super().__init__(*args, **kwargs)
        if encounter:
            self.fields['target'].queryset = Combatant.objects.filter(encounter=encounter)

class HealForm(forms.Form):
    healer = forms.ModelChoiceField(queryset=Combatant.objects.all(), widget=forms.HiddenInput())
    target = forms.ModelChoiceField(queryset=Combatant.objects.all())
    amount = forms.IntegerField(min_value=0)

    def __init__(self, *args, **kwargs):
        encounter = kwargs.pop('encounter', None)
        super().__init__(*args, **kwargs)
        if encounter:
            self.fields['target'].queryset = Combatant.objects.filter(encounter=encounter)
from django import forms
from .models import Hero, Enemy, Encounter, Combatant

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


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        exclude = ('current_hp',)
        widgets = {
            'game_session': forms.HiddenInput(),
        }

class EnemyForm(forms.ModelForm):
    class Meta:
        model = Enemy
        fields = '__all__'
        widgets = {
            'game_session': forms.HiddenInput(),
        }

class EncounterForm(forms.ModelForm):
    class Meta:
        model = Encounter
        fields = ['name', 'description', 'game_session']
        widgets = {
            'game_session': forms.HiddenInput(),
        }

from django import forms
from django.contrib.auth.models import User
from voting.models import Voting

class CensusForm(forms.Form):

    t_ids = tuple((u.get('id'), "Id: "+str(u.get('id'))+" Nombre: "+str(u.get('first_name'))) for u in User.objects.values())

    voting_id = forms.IntegerField(min_value=1)

    #num_choices = ( ("ONE"), ("TWO"), ("Three"), ("Four"))

    voter_ids = forms.MultipleChoiceField(choices=t_ids, required=True, widget=forms.CheckboxSelectMultiple(), label='Select No')

class FilteredCensusForm(forms.Form):
    voting = forms.ModelChoiceField(label='Open votings', empty_label="-", queryset=Voting.objects.all().filter(start_date__isnull=True, end_date__isnull=True), required=True)

    SEX_OPTIONS = (('Man', 'Man'), ('Woman', 'Woman'), ('DK/NA', 'DK/NA'))
    sex = forms.MultipleChoiceField(label='Sex', choices=SEX_OPTIONS, required=False)

    city = forms.CharField(label='City', widget=forms.TextInput(), required=False)

    init_age = forms.DateField(label='Initial age', widget=forms.TextInput(attrs={'placeholder': 'Format: dd/mm/yyyy'}), input_formats=['%d/%m/%Y'], required=False)
    fin_age = forms.DateField(label='Final age', widget=forms.TextInput(attrs={'placeholder': 'Format: dd/mm/yyyy'}), required=False)

    PRIVILEGE_OPTIONS = ((True, 'Staff'),(False, 'Non-Staff'))
    privileges = forms.MultipleChoiceField(label='Privileges', choices=PRIVILEGE_OPTIONS, required=False)
from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from voting.models import Voting

class CensusForm(forms.Form):

    t_ids = tuple((u.get('id'), "Id: "+str(u.get('id'))+" Nombre: "+str(u.get('first_name'))) for u in User.objects.values())

    voting = forms.ModelChoiceField(label='Open votings', empty_label="-", queryset=Voting.objects.all().filter(end_date__isnull=True), required=True,
    widget=forms.Select(attrs={'style': 'width: 300px;','class': 'form-control'}))
    
    voter_ids = forms.MultipleChoiceField(choices=t_ids, required=True, widget=forms.CheckboxSelectMultiple(), label='Select No')
class FilteredCensusForm(forms.Form):
    voting = forms.ModelChoiceField(label='Open votings', empty_label="-", queryset=Voting.objects.all().filter(end_date__isnull=True), required=True,
    widget=forms.Select(attrs={'style': 'width: 300px;','class': 'form-control'}))

    SEX_OPTIONS = (('Man', 'Man'), ('Woman', 'Woman'), ('DK/NA', 'DK/NA'))
    sex = forms.MultipleChoiceField(label='Sex',choices=SEX_OPTIONS, required=False,
    widget=forms.SelectMultiple(attrs={'style': 'width: 110px;','class': 'form-control'}))

    city = forms.CharField(label='City', required=False,
    widget=forms.TextInput(attrs={'style': 'width: 150px;','class': 'form-control'}))

    init_age = forms.DateField(label='Initial age', widget=forms.TextInput(attrs={'placeholder': 'Format: dd/mm/yyyy', 'style': 'width: 200px;','class': 'form-control'}), 
    input_formats=['%d/%m/%Y'], required=False)

    fin_age = forms.DateField(label='Final age', widget=forms.TextInput(attrs={'placeholder': 'Format: dd/mm/yyyy','style': 'width: 200px;','class': 'form-control'}),
    input_formats=['%d/%m/%Y'],required=False)
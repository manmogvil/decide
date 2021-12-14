from django import forms
from django.contrib.auth.models import User

class CensusForm(forms.Form):

    t_ids = tuple((u.get('id'), "Id: "+str(u.get('id'))+" Nombre: "+str(u.get('first_name'))) for u in User.objects.values())

    voting_id = forms.IntegerField(min_value=1)

    #num_choices = ( ("ONE"), ("TWO"), ("Three"), ("Four"))

    voter_ids = forms.MultipleChoiceField(choices=t_ids, required=True, widget=forms.CheckboxSelectMultiple(), label='Select No')

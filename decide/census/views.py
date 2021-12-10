from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Census
from . import forms
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff

from django.contrib.auth.models import User
from voting.models import Voting
from django.utils import timezone
from django.contrib import messages

has_voting_started = lambda v: v.start_date == None or v.start_date > timezone.now()

def add_to_census(request, voting_id, voters, new_logic_checks = None):
    #Generalized function to add the voters in the list to the census
    votings = [v for v in list(Voting.objects.all()) if v.id == int(voting_id)]

    #List of evaluations to verify, if it's true proceed, otherwise return the error message
    logic_checks = [[request.user.is_staff, 'Access denied'],
                    [votings, 'Voting id does not exist'],
                    #[not has_voting_started(votings[0]), 'Voting has already started']
                    [voters, 'No users to add to the census']
                    ]

    if new_logic_checks:
        logic_checks += new_logic_checks

    for check in logic_checks:
        if not check[0]:
            messages.add_message(request, messages.ERROR, check[1])

    if not all(check[0] for check in logic_checks):
        return HttpResponseRedirect('/admin/census') 

    for voter in voters:
        try:
            census = Census(voting_id=voting_id, voter_id=voter.id)
            census.save()
        except:
            return HttpResponseRedirect('/admin')
    return HttpResponseRedirect('/admin/census')

def add_filtered(request):
    if request.method == 'POST': 
        form = forms.FilteredCensusForm(request.POST)
        if form.is_valid():
            voting_id = form.cleaned_data['voting_id']
            selected_privilege = form.cleaned_data['privileges']
            voters = User.objects.filter(is_staff=selected_privilege == ['True'])
            return add_to_census(request, voting_id, voters)
    else:
        form = forms.FilteredCensusForm()
    return render(request, 'create_census_filters.html', {'form':form})


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

def create_census(request):
    if request.method == 'POST':
        form = forms.CensusForm(request.POST)
        if form.is_valid():
            voting_id = form.cleaned_data['voting_id']
            voter_ids = form.cleaned_data['voter_ids']
            for voter_id in voter_ids:
                print(voter_id)
                try:
                    census = Census(voting_id=voting_id, voter_id=voter_id)
                    census.save()
                except IntegrityError:
                    return HttpResponseRedirect('/admin/census')
            return HttpResponseRedirect('/admin/census')
    else:
        form = forms.CensusForm()
    return render(request, 'create_census.html', {'form':form})
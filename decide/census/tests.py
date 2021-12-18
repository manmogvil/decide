import random
from django.contrib.auth.models import User
from django.test import TestCase
from authentication.models import Profile

from rest_framework.test import APIClient
from django.core.serializers import json
from .forms import CensusForm
from .models import Census
from base import mods
from base.tests import BaseTestCase
from voting.models import Question, Voting

class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        question1 = Question.objects.create(desc='Question 1')
        voting1 = Voting.objects.create(id=10, name='Voting', question = question1)
        voting1.save()

        self.census = Census(voting_id=10, voter_id=1)
        self.census.save()

    
    def tearDown(self):
        super().tearDown()
        self.census = None
    
    '''
    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [1]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())'''
    '''
    def test_add_all_voters(self):
        census_before = len(Census.objects.all().values_list('voting_id', flat=True))
        
        self.client.login(user='admin')
        data = {'voting': 10, 'voter_ids': 1}
        response = self.client.post('http://localhost:8000/admin/census/addCustom/', data, format='json')
        census_after = len(Census.objects.all().values_list('voting_id', flat=True))
        
        
        print('----------------------------------------------------------------------\n')
        print(Voting.objects.all().values())
        print(User.objects.all())
        print(census_before, census_after)
        print(response)
        print('\n----------------------------------------------------------------------\n')
        #self.assertEqual(response.status_code, 302)
        self.assertTrue(census_after > census_before)

    '''
    
    def test_add_voter_custom_post(self): 
 
        admin = User(username='admin2', password='qwerty')
        admin.is_staff = True
        admin.save()
        self.client.force_login(admin)
        response = self.client.post('/census/addCustom/', 
        data={'voting': ['10'], 'voter_ids': ['2']})

        census = Census.objects.all()
        
        print('----------------------------------------------------------------------\n')
        print('Census: ', census)
        print(response)
        print('\n----------------------------------------------------------------------\n')
      
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(census), 2)

    
    def test_add_voter_custom_get(self):

        admin = User(username='admin2', password='qwerty')
        admin.is_staff = True
        admin.save()
        self.client.force_login(admin)
        response = self.client.get('/census/addCustom/')
        self.assertEqual(response.status_code, 200)
    
    def test_add_filters_post(self):
        admin = User(username='admin2', password='qwerty')
        admin.is_staff = True
        perfil = Profile(user=admin, sex='Man', location='Sevilla', birth_date='1999-10-10')
        admin.save()
        perfil.save()
        self.client.force_login(admin)
        '''response = self.client.post('http://localhost:8000/admin/census/addFilters/', 
        data={'voting': ['10'], 'sex': ['Man'], 'city': [''], 'init_age': [''], 'fin_age': ['']})
        census = Census.objects.all()
        
        print('----------------------------------------------------------------------\n')
        print('Census: ', census)
        print(response)
        print('\n----------------------------------------------------------------------\n')
      
        #self.assertEqual(response.status_code, 302)
        self.assertEqual(len(census), 2)'''


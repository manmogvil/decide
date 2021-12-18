from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

    def save(self, *args, **kwargs):
        user_added = User.objects.filter(id=self.voter_id).values()
        if(user_added):
            nombre = str(user_added[0].get('first_name'))
            email = str(user_added[0].get('email'))
            
            send_mail(
            'Añadido al censo de una votación',
            'Hola '+nombre+' acabas de ser añadido como participante en una votación, para acceder a ella entra en http://localhost:8000/booth/'+str(self.voting_id)+'/',
            None,
            [email],
            fail_silently=False,
            )


        return super().save()
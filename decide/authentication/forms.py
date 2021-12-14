from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User


from nocaptcha_recaptcha.fields import NoReCaptchaField


#Formulario para editar usuario existentes
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sex', 'location', 'birth_date')
        widgets = {
            'birth_date': forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}),
        }


#Formulario para crear nuevos usuarios
class RegisterUserForm(UserCreationForm):
    SEX_CHOICES = (
        ('Man', 'Man'),
        ('Woman', 'Woman'),
        ('DK/NA', 'DK/NA')
    )
    
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)
    sex=forms.ChoiceField(choices=SEX_CHOICES)
    location = forms.CharField(max_length=140, required=False)
    birth_date = forms.DateField (required=False, widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}))

    captcha = NoReCaptchaField()

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'sex',   
	        'location',
	        'birth_date',
            'password1',
            'password2',
        )
        widgets = {
            'birth_date': forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}),
        }


    # Check unique email
    # Email exists && account active -> email_already_registered
    # Email exists && account not active -> delete previous account and register new one
    def clean_email(self):
        email_passed = self.cleaned_data.get("email")
        email_already_registered = User.objects.filter(email = email_passed).exists()
        user_is_active = User.objects.filter(email = email_passed, is_active = 1)
        if email_already_registered and user_is_active:
            #print('email_already_registered and user_is_active')
            raise forms.ValidationError("Email already registered.")
        elif email_already_registered:
            #print('email_already_registered')
            User.objects.filter(email = email_passed).delete()

        return email_passed
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, RegisterView, register, activate


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    
    path('registerUser/', register, name='registerUser'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
    path('accounts/', include('django.contrib.auth.urls')),
]

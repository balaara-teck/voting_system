from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('voter_register/<int:pk>', views.VoterRegisterView.as_view(), name='voter_register'),
    path("voter_card/",views.voter_card,name="votercard"),
    path("election_officer/",views.ElectorialCommissionOfficerView.as_view(),name="election-Officer"),
]
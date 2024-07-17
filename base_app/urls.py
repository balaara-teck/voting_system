from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('voter_register/<str:pk>', views.VoterRegisterView.as_view(), name='voter_register'),
    path("voter_card/",views.voter_card,name="votercard"),
    path("logout/",views.logout_view,name="logout"),
    path("my_elections/",views.ElectorialCommissionOfficerView.as_view(),name="my_elections"),
    path("my_elections/<str:pk>/voters",views.voters.as_view(),name="voters"),
    path('portfolios/<int:pk>', views.PortfolioView.as_view(), name='portfolios'),
    path('candidates/<int:pk>', views.CandidateView.as_view(), name='candidates'),

]
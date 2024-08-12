from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import VoterRegistrationModel,ElectorialCommissionOfficerModel,PortfolioModel,CandidateModel,AccessElectionModel


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
 

class UserLoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password']
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
   
class ElectorialCommissionOfficerForm(forms.ModelForm):
    class Meta:
        model = ElectorialCommissionOfficerModel
        fields = ["election_name"]
    election_name = forms.CharField( widget=forms.TextInput(attrs={'placeholder': " Enter Election's Name" }))
    
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = PortfolioModel
        fields = ["portfolio_name"]
    portfolio_name = forms.CharField(label='Portfolio Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter portfolio name. e.g President'}))
    
class CandidateForm(forms.ModelForm):
    class Meta:
        model = CandidateModel
        fields = ["email","portfolio_name"]
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

class AccessElectionForm(forms.ModelForm):
    class Meta:
        model = AccessElectionModel
        fields = ["election_name","voter_id","email"]
    election_name = forms.CharField(label='Election Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter Election Name'}))
    voter_id = forms.CharField(label='Voter ID:', widget=forms.TextInput(attrs={'placeholder': 'Enter Voting ID'}))
    email = forms.CharField(label='Email:', widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email'}))
   

class VoterRegisterationForm(forms.ModelForm):
    class Meta:
        model = VoterRegistrationModel
        fields = ['first_name', 'last_name',"email", 'date_of_birth', 'address', 'city', 'state',
                   'zip_code', 'phone_number']




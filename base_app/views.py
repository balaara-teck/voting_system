
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm,UserRegistrationForm,VoterRegisterationForm,ElectorialCommissionOfficerForm
from django.views.generic import CreateView
from .models import VoterRegistrationModel,ElectionDayModel,ElectorialCommissionOfficerModel
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import string

def voter_card(request):
    try:
        voter = VoterRegistrationModel.objects.get(user=request.user)
        return render(request, 'voter_card.html', {'voter': voter})
    except:
        voter = None    
        return render(request, 'voter_card.html', {'voter': None})
    

class VoterRegisterView(LoginRequiredMixin,CreateView):
    model = VoterRegistrationModel
    form_class = VoterRegisterationForm
    template_name = 'register_voter.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("home")
 
    def form_valid(self, form,pk):
        form.instance.election_name = ElectorialCommissionOfficerModel.objects.get(id = pk)
        form.instance.voter_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return super().form_valid(form)
    
class ElectorialCommissionOfficerView(LoginRequiredMixin, CreateView):
    model = ElectorialCommissionOfficerModel
    form_class = ElectorialCommissionOfficerForm
    template_name = 'election_officer.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add existing elections to the context
        context['existing_elections'] = ElectorialCommissionOfficerModel.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.election_name = form.instance.election_name.lower()
        if ElectorialCommissionOfficerModel.objects.filter(election_name=form.instance.election_name, user=self.request.user).exists():
            form.add_error('election_name', f'{self.request.user.username.capitalize()}, you already have an election account with the name "{form.instance.election_name}"')
            return self.form_invalid(form)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        # If the user selects an existing election, redirect to the success URL
        if 'existing_election' in request.POST:
            existing_election_id = request.POST.get('existing_election')
            if ElectorialCommissionOfficerModel.objects.filter(id=existing_election_id, user=request.user).exists():
                return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
    

    
def home(request):
   return render(request, 'base_template.html')

def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return home(request)  # Redirect to a success page
    return render(request, 'register_login.html', {'form': form})

def register(request):
    tempate = 'register.html'
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')     
    return render(request, 'register_login.html', {'form': form,"template":tempate})


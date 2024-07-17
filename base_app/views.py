from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import UserLoginForm,UserRegistrationForm,VoterRegisterationForm,ElectorialCommissionOfficerForm,PortfolioForm,CandidateForm
from django.views.generic import CreateView
from .models import VoterRegistrationModel,ElectorialCommissionOfficerModel,PortfolioModel,CandidateModel
from django.urls import reverse_lazy,reverse
from django.views.generic import View
from django.contrib import messages
from django.views.generic import ListView 
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import string




def home(request):
   portfolios = PortfolioModel.objects.all()
   return render(request, 'index.html',{'portfolios': portfolios})

def voter_card(request):
    try:
        voter = VoterRegistrationModel.objects.get(user=request.user)
        return render(request, 'voter_card.html', {'voter': voter})
    except:
        voter = None    
        return render(request, 'voter_card.html', {'voter': None})
    
class CandidateView(CreateView):
    model = CandidateModel
    form_class = CandidateForm
    template_name = "candidate.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        pk = self.kwargs.get("pk")
        election = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user,id=pk)
        form.fields["portfolio_name"].queryset = PortfolioModel.objects.filter(election_name=election)
        candidates= CandidateModel.objects.filter(election_name=election) 
        return render(request, self.template_name, {"form": form, "candidates":candidates})
        
    def form_valid(self, form):    
        pk = self.kwargs.get("pk")
        election = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user,id=pk)
        if not VoterRegistrationModel.objects.filter(election_name=election,email=form.instance.email).exists():
            form.add_error("email","Candidate must be a registered voter!")
            return self.form_invalid(form)
        form.instance.election_name = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user, id=pk)
        form.instance.candidate = get_object_or_404(
            VoterRegistrationModel,
            email=form.instance.email,
            election_name=form.instance.election_name,
            )
       
        if CandidateModel.objects.filter(  
            portfolio_name=form.instance.portfolio_name,
            candidate=form.instance.candidate
            ).exists():
            form.add_error("email","This candidate has already been registered!")
            return self.form_invalid(form)
        
        elif CandidateModel.objects.filter(email=form.instance.email).exists():
            form.add_error("email","One candidate cannot register for two portfolios!")
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs.get("pk")
        return reverse("candidates",kwargs={"pk":pk})

class PortfolioView(CreateView):
    model=PortfolioModel
    form_class = PortfolioForm
    template_name="portfolio.html"


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        election = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user,id=pk) 
        context["portfolios"] = PortfolioModel.objects.filter(election_name=election)
        return context

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        election = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user,id=pk)
        form.instance.election_name = election
        form.instance.portfolio_name = form.instance.portfolio_name.capitalize() 
        if PortfolioModel.objects.filter(election_name=election,portfolio_name=form.instance.portfolio_name).exists():
            form.add_error("portfolio_name","This portfolio already exist")
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk")
        return reverse("portfolios",kwargs={"pk":pk})


class VoterRegisterView(LoginRequiredMixin, View):
    form_class = VoterRegisterationForm
    template_name = 'register_voter.html'
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        election = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user,id=pk)
        voters = VoterRegistrationModel.objects.filter(election_name=election)
        voters = len(voters)
        return render(request, self.template_name,
                      {
                        "voters":voters,"election":election
                        }
                    )
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        pk = self.kwargs.get('pk')
        election = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user,id=pk)
        if form.is_valid():        
            form.instance.election_name = election
            form.instance.voter_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            form.save()
            messages.success(request,"Voter is registered successfully.")
            return self.form_valid(form)
        voters = VoterRegistrationModel.objects.filter(election_name=election)
        voters = len(voters)
        return render(request, self.template_name,{'form': form,"voters":voters,"election":election})

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        return redirect(reverse('voter_register', kwargs={'pk': pk}))
    
class ElectorialCommissionOfficerView(LoginRequiredMixin, CreateView):

    model = ElectorialCommissionOfficerModel
    form_class = ElectorialCommissionOfficerForm
    template_name = 'my_elections.html'
    login_url = reverse_lazy("login")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_elections'] = ElectorialCommissionOfficerModel.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.election_name = form.instance.election_name.lower()
        if ElectorialCommissionOfficerModel.objects.filter(election_name=form.instance.election_name).exists():
            form.add_error('election_name', f'{self.request.user.username.capitalize()}, an election account with the name "{form.instance.election_name}" exists')
            return self.form_invalid(form)
        return super().form_valid(form)
       
    def get_success_url(self):
        return reverse('voter_register', kwargs={'pk': self.object.pk})


class voters(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")
    template_name = "my_voters.html"

    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get("pk")
        election = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user,id=pk)
        voters = VoterRegistrationModel.objects.filter(election_name=election)
        return render(request,self.template_name,{"voters":voters})

    

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
                return redirect("my_elections")  # Redirect to a success page
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

def logout_view(request):
    logout(request)
    return redirect("home")


        


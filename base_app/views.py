
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import UserLoginForm,UserRegistrationForm,VoterRegisterationForm,ElectorialCommissionOfficerForm,PortfolioForm,CandidateForm,AccessElectionForm
from django.views.generic import CreateView
from .models import VoterRegistrationModel,VoterModel,ElectorialCommissionOfficerModel,PortfolioModel,CandidateModel,AccessElectionModel
from django.urls import reverse_lazy,reverse
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import string




class AccessElectionView(View):
    model = AccessElectionModel
    form_class = AccessElectionForm
    template_name = "voter-identifier.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            election = form.cleaned_data['election_name'].upper()
            voter_id = form.cleaned_data['voter_id']
            email = form.cleaned_data['email']

            if not ElectorialCommissionOfficerModel.objects.filter(election_name=election).exists() or  not VoterRegistrationModel.objects.filter(
                election_name=get_object_or_404(ElectorialCommissionOfficerModel,election_name=election),
                voter_id=voter_id,
                email=email
                ).exists():
                form.add_error('election_name', 'Your credentials are invalid')
                return render(request, self.template_name, {'form': form})
            else:
                self.request.session['election_name'] = election
                self.request.session['voter_id'] = voter_id
                self.request.session['email'] = email
                return redirect('start_voting')
        return render(request, self.template_name, {'form': form}) 

class StartVotingView(View):
    template_name = "start_voting.html"

    def get(self, request, *args, **kwargs):
        election = request.session.get('election_name')
        voter_id = request.session.get('voter_id')
        email = request.session.get('email')
        voter = get_object_or_404(VoterRegistrationModel,email=email)

        areas_contested = PortfolioModel.objects.filter(
            election_name=get_object_or_404(ElectorialCommissionOfficerModel, election_name=election)
        )

        current_index = request.session.get(voter_id, 0)
       
        if current_index >= len(areas_contested):
            request.session[voter_id] = 0 
            voter.is_voted = True
            voter.save()
            return render(request, 'voting_complete.html')
        
        if voter.is_voted == True:
            return render(request, 'voting_complete.html')

        current_portfolio = areas_contested[current_index]
        contestants = CandidateModel.objects.filter( portfolio_name=current_portfolio)
        no_of_contestants = len(contestants)

        if not contestants:
            request.session[voter_id] = request.session.get(voter_id, 0) + 1   
            return redirect('start_voting')

        return render(request, self.template_name, {
            'contestants': contestants,
            'area_contested': current_portfolio,
            "no_of_contestants":no_of_contestants,
            
        })

    def post(self, request, *args, **kwargs):
        voter_id = request.session.get('voter_id')
        contestant_email = request.POST.get('email')
        if contestant_email:
            if "yes" in contestant_email or "no" in contestant_email:
                if contestant_email.split(' ')[1] == 'yes':
                    contestant = get_object_or_404(CandidateModel, email=contestant_email.split(" ")[0])
                    contestant.votes += 1
                    contestant.save()
                else:
                    pass
            else:
                contestant = get_object_or_404(CandidateModel, email=contestant_email)
                contestant.votes += 1
                contestant.save()
        else:
            return redirect('start_voting')

                
        request.session[voter_id] = request.session.get(voter_id, 0) + 1   
        return redirect('start_voting')
          
def home(request):
   c_election = request.session.get('election_name')
   portfolios = PortfolioModel.objects.all()
   return render(request, 'index.html',{'portfolios': portfolios,"c_election":c_election})

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
        no_of_voters = len(VoterRegistrationModel.objects.filter(election_name=election))
        form.fields["portfolio_name"].queryset = PortfolioModel.objects.filter(election_name=election)
        candidates= CandidateModel.objects.filter(election_name=election) 
        return render(request, self.template_name, {"form": form, "candidates":candidates,"election":election,"no_of_voters":no_of_voters,"template_name":self.template_name})
        
    def form_valid(self, form):    
        pk = self.kwargs.get("pk")
        election = get_object_or_404(ElectorialCommissionOfficerModel,user=self.request.user,id=pk)
        no_of_voters = len(VoterRegistrationModel.objects.filter(election_name=election))
        if not VoterRegistrationModel.objects.filter(election_name=election,email=form.instance.email).exists():
            form.add_error("email","Candidate must be a registered voter!")
            candidates = CandidateModel.objects.filter(election_name=election)
            return render(self.request, self.template_name, {"form": form, "candidates": candidates,"election":election,"no_of_voters":no_of_voters,"template_name":self.template_name})

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
            candidates = CandidateModel.objects.filter(election_name=election)
            return render(self.request, self.template_name, {"form": form, "candidates": candidates,"election":election,"no_of_voters":no_of_voters,"template_name":self.template_name})

        elif CandidateModel.objects.filter(email=form.instance.email).exists():
            form.add_error("email","One candidate cannot register for two portfolios!")
            candidates = CandidateModel.objects.filter(election_name=election)
            return render(self.request, self.template_name, {"form": form, "candidates": candidates,"election":election,"no_of_voters":no_of_voters,"template_name":self.template_name})
        return super(CandidateView,self).form_valid(form)
    
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
        context["election"] = election
        context["no_of_voters"] = len(VoterRegistrationModel.objects.filter(election_name=election))
        context["template_name"] = "portfolio.html"
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
        no_of_voters = len(voters)
        return render(request, self.template_name,
                      {
                        "no_of_voters":no_of_voters,"election":election,"election_name":election.election_name.upper()
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
        no_of_voters = len(voters)
        return render(request, self.template_name,{'form': form,"no_of_voters":no_of_voters,"election":election})

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
        form.instance.election_name = form.instance.election_name.upper()
        if len(form.instance.election_name) < 3:
            form.add_error('election_name', f"{self.request.user.username.capitalize()}, at least three characters are required for election's name")
            return self.form_invalid(form)
        elif ElectorialCommissionOfficerModel.objects.filter(election_name=form.instance.election_name).exists():
            form.add_error('election_name', f'{self.request.user.username.capitalize()}, an election account with the name "{form.instance.election_name}" already exists')
            return self.form_invalid(form)
        elif len(ElectorialCommissionOfficerModel.objects.filter(user=self.request.user)) >= 5:
            form.add_error('election_name', f"{self.request.user.username.capitalize()}, you can't have more than five election. Cosinder deleting one.")
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
        no_of_voters = len(voters)
        context = {"no_of_voters":no_of_voters,"voters":voters,"election":election,"template":"my_voters.html"}
        return render(request,self.template_name,context) 

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
                return redirect("my_elections")
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'register_login.html', {'form': form})
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


        


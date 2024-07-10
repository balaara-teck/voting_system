from django.db import models
from django.contrib.auth.models import User

class ElectorialCommissionOfficerModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    election_name = models.CharField(max_length=200, null=False)
    date_deployed = models.DateField(auto_now_add=True)    
    def __str__(self):
        return self.election_name
        
class PortfolioModel(models.Model):
    portfolio_name = models.CharField(max_length=255)
    election_name = models.ForeignKey(ElectorialCommissionOfficerModel, on_delete=models.CASCADE)
    def __str__(self):
        return self.portfolio_name

class VoterRegistrationModel(models.Model):
    election_name = models.ForeignKey(ElectorialCommissionOfficerModel, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    voter_id = models.CharField(max_length=10,unique=True)
    # photo = models.ImageField()
    # bymetrics = models.BinaryField()
    date_registed = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.first_name + " " + self.last_name
    
class CandidateModel(models.Model):
    candidate = models.ForeignKey(VoterRegistrationModel, on_delete=models.CASCADE)
    election_name = models.ForeignKey(ElectorialCommissionOfficerModel, on_delete=models.CASCADE)
    portfolio_name = models.ForeignKey(PortfolioModel, on_delete=models.CASCADE)
    email = models.EmailField()# for filtering candidate in VoterRegistrationModel
    def __str__(self):
        return f"{self.candidate}" 
    
class VoterModel(models.Model):
    voter = models.ForeignKey(VoterRegistrationModel, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE)
    portfolio_name = models.ForeignKey(PortfolioModel, on_delete=models.CASCADE)
    time_voted = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.voter}"
    
class StartEctionModel(models.Model):
    election_name = models.ForeignKey(ElectorialCommissionOfficerModel, on_delete=models.CASCADE)
    start_time = models.DateField(auto_now_add=True)
    end_time = models.DateField()
    def __str__(self):
        return f"{self.election_name}"
    
class AccessElectionModel(models.Model):
    election_name = models.ForeignKey(ElectorialCommissionOfficerModel, on_delete=models.CASCADE)
    access_time = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.election_name}"

 





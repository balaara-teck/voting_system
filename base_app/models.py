from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ElectorialCommissionOfficerModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    election_name = models.CharField(max_length=200, null=False)
    date_deployed = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.election_name


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






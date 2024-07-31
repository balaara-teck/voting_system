from django.contrib import admin
from .models import VoterRegistrationModel,ElectorialCommissionOfficerModel,PortfolioModel,CandidateModel


# Register your models here.
admin.site.register(VoterRegistrationModel)
admin.site.register(ElectorialCommissionOfficerModel)
admin.site.register(PortfolioModel)
admin.site.register(CandidateModel)







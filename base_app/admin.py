from django.contrib import admin
from .models import VoterRegistrationModel,ElectorialCommissionOfficerModel,PortfolioModel


# Register your models here.
admin.site.register(VoterRegistrationModel)
admin.site.register(ElectorialCommissionOfficerModel)
admin.site.register(PortfolioModel)



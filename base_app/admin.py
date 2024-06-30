from django.contrib import admin
from .models import VoterRegistrationModel,ElectionDayModel,ElectorialCommissionOfficerModel

# Register your models here.
admin.site.register(VoterRegistrationModel)
admin.site.register(ElectorialCommissionOfficerModel)
admin.site.register(ElectionDayModel)


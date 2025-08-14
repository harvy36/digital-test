from django.contrib import admin
from apps.users.models import Member, Loan

# Register your models here.
admin.site.register(Member)
admin.site.register(Loan)

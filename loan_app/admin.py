from django.contrib import admin

from loan_app.apps.users.models import User
from loan_app.apps.loans.models import Loan


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Loan)
class QuizAdmin(admin.ModelAdmin):
    pass


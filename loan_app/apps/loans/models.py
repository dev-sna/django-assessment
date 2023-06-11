from django.db import models

from loan_app.apps.users.models import User

class Loan(models.Model):
    LOAN_PENDING = "PND"
    LOAN_APPROVED = "APR"
    LOAN_REJECTED = "REJ"

    LOAN_STATUS_CHOICES = (
        (LOAN_APPROVED, 'Pending'),
        (LOAN_APPROVED, 'Approved'),
        (LOAN_APPROVED, 'Rejected'),
    )

    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(
        max_length=3,
        choices=LOAN_STATUS_CHOICES,
        default=LOAN_PENDING,
    )
    comment = models.CharField(max_length=200, blank=True, null=True)
    amount_paid = models.IntegerField(default=0)
    is_fully_paid = models.BooleanField(default=False)
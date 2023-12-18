from re import M
from django.db import models

class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=255)

    def __str__(self):
        return f'Donation #{self.id} - {self.name} ({self.amount})'
    

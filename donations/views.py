from django.shortcuts import render, redirect
from .forms import DonationForm
from .models import Donation
from payfast.signals import payment_successful
from django.dispatch import receiver

def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            # Save donation information to the database
            donation = Donation(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                amount=form.cleaned_data['amount'],
                transaction_id='unique_transaction_id',  # Generate a unique ID
            )
            donation.save()

            # Redirect to PayFast payment page
            # (Note: Replace 'merchant_id' and 'merchant_key' with your PayFast credentials)
            return render(request, 'donate/payment_page.html', {
                'donation': donation,
                'merchant_id': 'your_merchant_id',
                'merchant_key': 'your_merchant_key',
            })
    else:
        form = DonationForm()

    return render(request, 'donations/donation_form.html', {'form': form})


@receiver(payment_successful)
def handle_payment_success(sender, **kwargs):
    # Handle successful payment, update your database, send confirmation emails, etc.
    transaction_id = kwargs['transaction_id']
    donation = Donation.objects.get(transaction_id=transaction_id)
    # Update donation status or perform other actions

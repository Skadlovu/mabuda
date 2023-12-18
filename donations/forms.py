from django import forms

class DonationForm(forms.Form):
    amount = forms.DecimalField(
        label='Donation Amount',
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter the donation amount'}),
    )
    name = forms.CharField(
        label='Your Name',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}),
    )
    email = forms.EmailField(
        label='Your Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
    )

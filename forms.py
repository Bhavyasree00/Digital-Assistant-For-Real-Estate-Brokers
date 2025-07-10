from django import forms
from .models import Inquiry, Transaction

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'message']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['property', 'document']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from apps.order.models import CustomerAddress


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)

    class Meta:
        model = get_user_model()
        fields = (
            'first_name', 'last_name', 'phone', 'city', 'postcode', 'address'
        )

    def get_user_address(self, user):
        return CustomerAddress.objects.filter(customer=user).first()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        if address := self.get_user_address(self.instance):
            self.fields['phone'].initial = address.phone
            self.fields['city'].initial = address.city
            self.fields['postcode'].initial = address.postcode
            self.fields['address'].initial = address.address

    def save(self, commit=True):
        user = super().save()
        address = self.get_user_address(user)
        if not address:
            address = CustomerAddress(customer=user)
            address.phone = self.cleaned_data['phone']
        address.phone = self.cleaned_data['phone']
        address.city = self.cleaned_data['city']
        address.postcode = self.cleaned_data['postcode']
        address.address = self.cleaned_data['address']
        address.save()
        return user

from django import forms

from apps.order.models import OrderAddress, CustomerAddress


class OrderBillingAddress(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = OrderAddress
        fields = (
            'first_name', 'last_name', 'phone', 'city', 'postcode', 'address'
        )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name

        if user.first_name:
            self.fields['first_name'].disabled = True
        self.fields['last_name'].initial = user.last_name

        if user.last_name:
            self.fields['last_name'].disabled = True

        if address := CustomerAddress.objects.filter(customer=user).first():
            self.fields['phone'].initial = address.phone
            self.fields['city'].initial = address.city
            self.fields['postcode'].initial = address.postcode
            self.fields['address'].initial = address.address

    def save(self, commit=True):
        billing_address = super().save(commit=commit)
        if "first_name" in self.changed_data:
            self.user.first_name = self.cleaned_data['first_name']
        if "last_name" in self.changed_data:
            self.user.last_name = self.cleaned_data['last_name']
        self.user.save()
        return billing_address

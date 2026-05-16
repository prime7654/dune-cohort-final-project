from django import forms

from .models import Order


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    phone_number = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields["full_name"].initial = user.get_full_name() or user.username
            self.fields["email"].initial = user.email

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_full_name(self):
        return self.cleaned_data["full_name"].strip()

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"].strip()
        if len(phone_number) < 7:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone_number

    def clean_email(self):
        return self.cleaned_data.get("email", "").strip().lower()

    def clean_delivery_address(self):
        delivery_address = self.cleaned_data["delivery_address"].strip()
        if not delivery_address:
            raise forms.ValidationError("Delivery address is required.")
        return delivery_address

    def clean_notes(self):
        return self.cleaned_data.get("notes", "").strip()


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs["class"] = "form-select form-select-sm"

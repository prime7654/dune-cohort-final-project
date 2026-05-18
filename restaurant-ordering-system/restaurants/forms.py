from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .auth_rate_limit import (
    AUTH_LOCKOUT_MESSAGE,
    clear_auth_failures,
    is_auth_locked,
    record_auth_failure,
)
from .models import MenuCategory, MenuItem

User = get_user_model()


def _apply_bootstrap_classes(form):
    for field_name, field in form.fields.items():
        if field_name == "is_available":
            field.widget.attrs["class"] = "form-check-input"
        else:
            field.widget.attrs["class"] = "form-control"


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_bootstrap_classes(self)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Category name is required.")
        return name

    def clean_description(self):
        return self.cleaned_data.get("description", "").strip()


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            "category",
            "name",
            "description",
            "price",
            "stock",
            "is_available",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_bootstrap_classes(self)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Menu item name is required.")
        return name

    def clean_description(self):
        return self.cleaned_data.get("description", "").strip()

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < Decimal("0.01"):
            raise forms.ValidationError("Price must be at least 0.01.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data["stock"]
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        name = cleaned_data.get("name")
        stock = cleaned_data.get("stock")
        is_available = cleaned_data.get("is_available")

        if stock == 0 and is_available:
            self.add_error(
                "stock",
                "Set stock above 0 or mark this menu item as unavailable.",
            )

        if not category or not name:
            return cleaned_data

        matching_items = MenuItem.objects.filter(
            category=category,
            name__iexact=name,
        )
        if self.instance.pk:
            matching_items = matching_items.exclude(pk=self.instance.pk)

        if matching_items.exists():
            self.add_error(
                "name",
                "A menu item with this name already exists in the selected category.",
            )

        return cleaned_data


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_bootstrap_classes(self)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Name is required.")
        return name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

        return cleaned_data

    def _unique_username(self):
        name = self.cleaned_data["name"]
        email = self.cleaned_data["email"]
        base_username = slugify(name) or email.split("@", 1)[0] or "user"
        base_username = base_username[:150]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            suffix = f"-{counter}"
            username = f"{base_username[:150 - len(suffix)]}{suffix}"
            counter += 1

        return username

    def save(self):
        user = User(
            username=self._unique_username(),
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["name"][:150],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or email")

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        _apply_bootstrap_classes(self)

    def clean(self):
        username = self.cleaned_data.get("username")
        rate_limit_username = username

        if username and "@" in username:
            matching_user = User.objects.filter(email__iexact=username).first()
            if matching_user:
                self.cleaned_data["username"] = matching_user.get_username()
                rate_limit_username = matching_user.get_username()

        if is_auth_locked(self.request, rate_limit_username):
            raise ValidationError(AUTH_LOCKOUT_MESSAGE, code="auth_locked")

        try:
            cleaned_data = super().clean()
        except ValidationError:
            locked = record_auth_failure(self.request, rate_limit_username)
            if locked:
                raise ValidationError(AUTH_LOCKOUT_MESSAGE, code="auth_locked")
            raise

        clear_auth_failures(self.request, rate_limit_username)
        return cleaned_data

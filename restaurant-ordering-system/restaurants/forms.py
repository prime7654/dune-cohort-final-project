from decimal import Decimal

from django import forms

from .models import MenuCategory, MenuItem


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
            "is_available",
            "image_url",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
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

    def clean_image_url(self):
        return self.cleaned_data.get("image_url", "").strip()

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        name = cleaned_data.get("name")

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

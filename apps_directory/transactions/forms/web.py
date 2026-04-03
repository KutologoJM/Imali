from django import forms

from apps_directory.transactions.models import (
    Account,
    AccountGroup,
    Category,
    Currency,
    Merchant,
    Transaction,
)


class BaseStyledModelForm(forms.ModelForm):
    class Meta:
        abstract = True

    def _apply_base_widget_classes(self):
        for field in self.fields.values():
            widget = field.widget
            existing_classes = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing_classes} input input-bordered w-full".strip()


class AccountGroupForm(forms.ModelForm):
    class Meta:
        model = AccountGroup
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "description": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 3}),
        }


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ["name", "currency_code", "currency_symbol", "locale"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "currency_code": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "currency_symbol": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "locale": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "group", "balance", "currency", "provider"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "group": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "balance": forms.NumberInput(attrs={"class": "input input-bordered w-full", "step": "0.01"}),
            "currency": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "provider": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
        }


class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ["name", "description", "is_global"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "description": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 3}),
            "is_global": forms.CheckboxInput(attrs={"class": "checkbox"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "type", "icon", "icon_color", "bg_color"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "description": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 3}),
            "type": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "icon": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "icon_color": forms.TextInput(attrs={"type": "color", "class": "input input-bordered w-full"}),
            "bg_color": forms.TextInput(attrs={"type": "color", "class": "input input-bordered w-full"}),
        }
        help_texts = {
            "icon": 'Browse icons at <a href="https://fontawesome.com/icons" target="_blank" rel="noopener" class="link link-primary">fontawesome.com</a>',
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "account",
            "destination_account",
            "merchant",
            "category",
            "amount",
            "status",
            "due_date",
            "date_paid",
            "description",
            "notes",
        ]
        widgets = {
            "account": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "destination_account": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "merchant": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "category": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "amount": forms.NumberInput(attrs={"class": "input input-bordered w-full", "step": "0.01"}),
            "status": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "due_date": forms.DateInput(attrs={"class": "input input-bordered w-full", "type": "date"}),
            "date_paid": forms.DateInput(attrs={"class": "input input-bordered w-full", "type": "date"}),
            "description": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 3}),
            "notes": forms.Textarea(attrs={"class": "textarea textarea-bordered w-full", "rows": 4}),
        }

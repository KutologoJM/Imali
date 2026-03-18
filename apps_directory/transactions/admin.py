"""
Registers models with the Django admin site.

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/admin/

Rules:
    - Register every model that needs to be managed via the admin interface.
    - Use ModelAdmin subclasses to customize list views, search, and filters.
    - Never put business logic here — admin actions should call services.

Example:
    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ["title", "author", "is_published", "created_at"]
        list_filter = ["is_published"]
        search_fields = ["title", "author__username"]
"""
from django.contrib import admin

from .models import Account, AccountGroup, Currency, Merchant, Category, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'user',
        'name',
        'group',
        'balance',
        'currency',
        'provider',
    )
    list_filter = ('created_at', 'updated_at', 'user', 'group', 'currency')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'name', 'description')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'name',
        'currency_code',
        'currency_symbol',
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'user',
        'name',
        'description',
        'is_global',
    )
    list_filter = ('created_at', 'updated_at', 'user', 'is_global')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'user',
        'name',
        'description',
        'type',
    )
    list_filter = ('created_at', 'updated_at', 'user')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'uuid',
        'user',
        'account',
        'destination_account',
        'merchant',
        'category',
        'amount',
        'status',
        'due_date',
        'date_paid',
        'description',
        'notes',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'user',
        'account',
        'destination_account',
        'merchant',
        'category',
        'due_date',
        'date_paid',
    )
    date_hierarchy = 'created_at'
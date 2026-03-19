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
        'icon',
        'icon_color',
        'bg_color',
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

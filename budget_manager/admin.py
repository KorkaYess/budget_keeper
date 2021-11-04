from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Account, Income, Outcome


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    mptt_indent_field = "name"
    list_display = ('name', 'type', 'slug', )
    prepopulated_fields = {'slug': ('name',)}
    mptt_level_indent = 20


class IncomeInline(admin.TabularInline):
    model = Income
    ordering = ['-created']
    readonly_fields = ['created', 'updated']
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('category', 'account', 'amount', )
        }),
        ('Timestamp', {
            'classes': ('collapse',),
            'fields': ('created', 'updated', )
        }),
    )


class OutcomeInline(admin.TabularInline):
    model = Outcome
    ordering = ['-created']
    readonly_fields = ['created', 'updated']
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('category', 'account', 'amount', )
        }),
        ('Timestamp', {
            'classes': ('collapse',),
            'fields': ('created', 'updated', )
        }),
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    model = Account
    inlines = [
        IncomeInline,
        OutcomeInline
    ]

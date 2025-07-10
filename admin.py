from django.contrib import admin
from .models import Property, Inquiry, Transaction

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'is_available', 'created_at')
    search_fields = ('title', 'city', 'address')
    list_filter = ('city', 'is_available', 'created_at')
    ordering = ('-created_at',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'property', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at', 'property')
    ordering = ('-created_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('property', 'uploaded_by', 'uploaded_at', 'compliance_status')
    search_fields = ('property__title', 'uploaded_by__username')
    list_filter = ('compliance_status', 'uploaded_at')
    ordering = ('-uploaded_at',)

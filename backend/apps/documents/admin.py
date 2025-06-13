from django.contrib import admin
from .models import Document, DocumentVersion, DocumentShare

class DocumentShareInline(admin.TabularInline):
    model = DocumentShare
    extra = 1

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'file_type', 'created_at')
    list_filter = ('is_public', 'file_type')
    search_fields = ('title', 'description')
    inlines = [DocumentShareInline]

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version_number', 'created_by')
    readonly_fields = ('version_number',)
from .models import Author, Quote, QuoteAndTag, Tag
from django.contrib import admin

# Register your models here.
class QuoteAdmin(admin.ModelAdmin):
  pass

class AuthorAdmin(admin.ModelAdmin):
  pass

class TagAdmin(admin.ModelAdmin):
  pass

class QuoteAndTagAdmin(admin.ModelAdmin):
  pass

admin.site.register(Quote, QuoteAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(QuoteAndTag, QuoteAndTagAdmin)
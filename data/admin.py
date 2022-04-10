from django.contrib import admin

from data.models import Data, Result

# Register your models here.
class ResultInLine(admin.TabularInline):
    model = Result
    extra = 1
    
class DataAdmin(admin.ModelAdmin):
    model = Data
    inlines = (ResultInLine,)
admin.site.register(Data,DataAdmin)
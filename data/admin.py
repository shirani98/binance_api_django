from django.contrib import admin

from data.models import Data, ArchiveData

# Register your models here.

    
class DataAdmin(admin.ModelAdmin):
    model = Data
admin.site.register(Data,DataAdmin)
admin.site.register(ArchiveData)
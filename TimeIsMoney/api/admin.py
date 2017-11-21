from django.contrib import admin
from model_realm.models import Realm

# Register your models here.
class RealmModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'isActive', 'lastModified', 'dateModified']
    list_filter = ["dateModified"]
    search_fields = ['name']
    class Meta:
        model = Realm

admin.site.register(Realm, RealmModelAdmin)

from django.contrib import admin

from core.models import Bus, Driver, Route

admin.site.register(Route)
admin.site.register(Bus)
admin.site.register(Driver)

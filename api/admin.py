from django.contrib import admin

# Register your models here.
from api.models import APIProduct, User

admin.site.register(User)


class APIProductAdmin(admin.ModelAdmin):

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['habibi'] = 'aanish'
        return super(APIProductAdmin, self).changeform_view(request, extra_context=extra_context)


admin.site.register(APIProduct, APIProductAdmin)

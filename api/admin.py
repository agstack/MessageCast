from django.contrib import admin

# Register your models here.
from api.models import APIProduct, User

admin.site.register(User)


class APIProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', )
    readonly_fields = ('total_subscribers', 'total_subscribers_by_country',
                       'total_subscribers_by_usage', )

    def total_subscribers(self, obj):

        return obj.subscribers.count()

    def total_subscribers_by_country(self, obj):
        total = 0
        # for itm in obj.subscribers.all():
        #     itm
        return total

    def total_subscribers_by_usage(self, obj):
        total = 0
        return total


admin.site.register(APIProduct, APIProductAdmin)

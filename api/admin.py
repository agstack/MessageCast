from api.models import APIProduct, User, Subscription
from api.serializers import SubscriptionMonthYearSerializer, SubscriptionCountrySerializer, SubscriptionUsageSerializer
from django import forms
from django.contrib import admin

admin.site.site_header = 'Agstack Admin Dashboard'
admin.site.register(User)
admin.site.register(Subscription)


class APIProductAdminnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(APIProductAdminnForm, self).__init__(*args, **kwargs)


class APIProductAdmin(admin.ModelAdmin):
    change_list_template = 'admin/api/apiproduct/change_list.html'
    list_display = ('name', 'active', )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        objs = Subscription.objects.filter(status=True).all()

        # monthly subscribers histogram
        objs_json = SubscriptionMonthYearSerializer(objs, many=True).data
        extra_context['month_year'] = [x['month_year'] for x in objs_json]

        # total subscribers
        total_subscribers = Subscription.objects.filter(status=True).count()
        extra_context['total_subscribers'] = total_subscribers

        # total_subscribers_by_country
        objs_json = SubscriptionCountrySerializer(objs, many=True).data
        extra_context['by_country'] = [x['country'] for x in objs_json]

        # total_subscribers_by_usage
        objs_json = SubscriptionUsageSerializer(objs, many=True).data
        extra_context['by_usage'] = [x['usage'] for x in objs_json]

        return super(APIProductAdmin, self).changelist_view(request, extra_context)


admin.site.register(APIProduct, APIProductAdmin)

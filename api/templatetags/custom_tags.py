from django.template.defaultfilters import register
from django.utils.safestring import mark_safe
import json


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

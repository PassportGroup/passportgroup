import json

from django import template

register = template.Library()


@register.filter(name='inertia_load')
def loads_inertia_json_data(value):
    return json.dumps(value)

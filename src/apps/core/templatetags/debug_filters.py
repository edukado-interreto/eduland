from django import template

register = template.Library()


@register.filter(name="dir")
def attributes(value):
    print(type(value))
    for attr in sorted(dir(value)):
        if not attr.startswith("__"):
            print(f"{attr}:", getattr(value, attr))
    return value

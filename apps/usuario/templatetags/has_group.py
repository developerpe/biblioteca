from django import template

register = template.Library()

@register.filter(name = 'has_group')
def has_group(usuario,grupo):
    return usuario.groups.filter(name__exact = grupo).exists()

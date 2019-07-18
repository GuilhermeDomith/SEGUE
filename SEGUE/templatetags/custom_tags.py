from django import template
from curso.models import NivelCurso
from django.apps import apps
from egresso.models import obter_egresso

register = template.Library()

@register.filter
def values(model_name):
    model = apps.get_model(model_name)
    return model.objects.values()

@register.filter
def get_egresso(user):
    return obter_egresso(user=user)

@register.filter
def get_opcoes_select(values, value_label):
    value_option,_, label_option = value_label.rpartition(':')
    opcoes=[]
    for v in values:
        opcao = dict(
            value= v[value_option],
            label= v[label_option]
        )
        opcoes.append(opcao)
    return opcoes
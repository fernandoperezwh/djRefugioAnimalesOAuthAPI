from django import template

register = template.Library()

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    if key: return dict_data.get(key)


@register.filter('join_vacunas')
def join_authores(lista_vacunas):
    string = ""
    for vacuna in lista_vacunas:
        string += "{}, ".format(vacuna.nombre)
    return string
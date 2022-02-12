# django packages
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
# third party packages
import requests
from requests import ConnectionError, ConnectTimeout


def build_form_input_attrs(key):
    return {
        "id": key,
        "aria-describedby": "{}_errors".format(key),
        "class": "form-control",
    }


def generic_api_delete(request, endpoint, instance, tpl_name, redirect, custom_messages={}):
    DEFAULT_SUCCESS_MESSAGE = "Se elimino el registro correctamente."
    DEFAULT_SERVER_CONNECTION_ERROR = 'Un error ha ocurrido intentando conectar con el servidor'
    if request.method == "POST":
        try:
            response = requests.delete(endpoint, cookies=request.COOKIES)
        except (ConnectionError, ConnectTimeout) as err:
            messages.error(request, DEFAULT_SERVER_CONNECTION_ERROR)
            return HttpResponseRedirect(redirect)
        # Se comprueba si se elimino el registro con exito
        if response.status_code != 204:
            messages.error(request, custom_messages.get('error'))
            return HttpResponseRedirect(redirect)
        # En este punto estamos seguros que se borro el registro e informamos al cliente
        messages.success(request, custom_messages.get('success') or DEFAULT_SUCCESS_MESSAGE)
        return HttpResponseRedirect(redirect)
    return render(request, tpl_name, {
        'object': instance,
        'redirect': redirect,
    })

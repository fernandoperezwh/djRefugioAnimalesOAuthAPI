# django packages
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView
# third party packages
import requests
from requests import ConnectionError, ConnectTimeout
from rest_framework import status
# local imports
from apps.adopcion.models import Persona
from apps.adopcion.forms import PersonaForm
from djRefugioAnimales.forms import SearchForm
from djRefugioAnimales.utils import generic_api_delete


# region persona - API Clase based views
class PersonaApiListView(ListView):
    endpoint = '{endpoint}/api/persona/'.format(endpoint=settings.API_ENDPOINT)
    model = Persona
    template_name = "adopcion__persona_listado.html"
    form_class = SearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        cd = dict()
        if form.is_valid():
            cd = form.cleaned_data
        return self.get_info_via_api(cd.get('q'))

    def get_context_data(self, **kwargs):
        context = super(PersonaApiListView, self).get_context_data(**kwargs)
        context['create_url'] = 'persona_new_api'
        context['edit_url'] = 'persona_edit_api'
        context['delete_url'] = 'persona_delete_api'
        context['buscador'] = self.form_class()
        return context

    def get_endpoint(self, search_query=None):
        if search_query:
            self.endpoint = "{endpoint}?q={q}".format(endpoint=self.endpoint, q=search_query)
        return self.endpoint

    def get_info_via_api(self, search_query=None):
        data = None
        try:
            response = requests.get(self.get_endpoint(search_query), cookies=self.request.COOKIES)
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return data

    def get(self, *args, **kwargs):
        if self.get_queryset() is None:
            return HttpResponseRedirect(reverse('home'))
        return super(PersonaApiListView, self).get(*args, **kwargs)


def persona_form_api(request, _id=None):
    RETURN_URL = 'persona_list_api'
    initial = {}
    # Se verifica la existencia
    if _id:
        try:
            endpoint = '{endpoint}/api/persona/{id}'.format(endpoint=settings.API_ENDPOINT, id=_id)
            response = requests.get(endpoint, cookies=request.COOKIES)
            if response.status_code != 200:
                raise Http404
            initial = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            messages.error(request, 'Un error a ocurrido consultando los datos de la persona con id: {id}'
                                    ''.format(id=_id))
            return HttpResponseRedirect(reverse(RETURN_URL))

    form = PersonaForm(initial=initial) if initial else PersonaForm()

    # Update/create
    if request.method == "POST":
        form = PersonaForm(request.POST, initial=initial)
        if form.is_valid():
            try:
                if initial:
                    # Se actualiza registro de persona
                    endpoint = '{endpoint}/api/persona/{id}/'.format(endpoint=settings.API_ENDPOINT, id=_id)
                    response = requests.put(endpoint, data=form.cleaned_data, cookies=request.COOKIES)
                else:
                    # Se crea registro de persona
                    endpoint = '{endpoint}/api/persona/'.format(endpoint=settings.API_ENDPOINT)
                    response = requests.post(endpoint, data=form.cleaned_data, cookies=request.COOKIES)

            except (ConnectionError, ConnectTimeout) as err:
                messages.error(request, 'Un error desconocido ha ocurrido intentando aplicar la accion sobre la '
                                        'persona <strong>{first_name} {last_name}</strong>'
                                        ''.format(first_name=form.cleaned_data.get('nombre'),
                                                  last_name=form.cleaned_data.get('apellidos')))
                return HttpResponseRedirect(reverse(RETURN_URL))

            # Se verifica si la api pudo actualizar los datos de la persona
            if response.status_code not in (200, 201):
                messages.error(request, 'Un error ha ocurrido intentando aplicar la accion sobre la persona '
                                        '<strong>{first_name} {last_name}</strong>'
                                        ''.format(first_name=form.cleaned_data.get('nombre'),
                                                  last_name=form.cleaned_data.get('apellidos')))
                return HttpResponseRedirect(reverse(RETURN_URL))
            # Si no ocurrio ningun error durante el intento de crear o eliminar, se manda el mensaje de exito
            messages.success(request, 'Se ha realizado con exito la accion sobre la persona <strong>{first_name} '
                                      '{last_name}</strong>'
                                      ''.format(first_name=form.cleaned_data.get('nombre'),
                                                last_name=form.cleaned_data.get('apellidos')))
            return HttpResponseRedirect(reverse(RETURN_URL))

    return render(request, "adopcion__persona_form.html", {
        "form": form,
    })


def persona_delete_api(request, _id):
    RETURN_URL = 'persona_list_api'
    endpoint = '{endpoint}/api/persona/{id}/'.format(endpoint=settings.API_ENDPOINT, id=_id)
    # Se intenta obtener el registro a eliminar
    try:
        response = requests.get(endpoint, cookies=request.COOKIES)
        if response.status_code != 200:
            raise Http404
        instance = response.json()
    except (ConnectionError, ConnectTimeout) as err:
        messages.error(request, 'Un error a ocurrido consultando los datos de la persona con id: {id}'
                                ''.format(id=_id))
        return HttpResponseRedirect(reverse(RETURN_URL))
    # Se manda a llamar las instrucciones genericas para eliminar en base al funcionamiento del api
    return generic_api_delete(
        request=request,
        endpoint=endpoint,
        instance=instance,
        tpl_name="adopcion__persona_delete.html",
        redirect=reverse(RETURN_URL),
        custom_messages={
            'success': 'Se elimino el registro de: <strong>{} {}</strong>'
                       ''.format(instance.get('nombre'), instance.get('apellidos')),
            'error': 'Un error ha ocurrido intentando eliminar el registro de: <strong>{} {}</strong>'
                     ''.format(instance.get('nombre'), instance.get('apellidos')),
        }
    )
# endregion

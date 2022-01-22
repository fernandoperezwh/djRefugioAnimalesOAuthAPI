# django packages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# third party packages
import requests
from requests import ConnectionError, ConnectTimeout

# local imports
from apps.adopcion.models import Persona
from apps.adopcion.forms import PersonaForm
from djRefugioAnimales.forms import SearchForm
from djRefugioAnimales.utils import generic_delete


# Create your views here.
def adopcion_index(request):
    return HttpResponse("Hello world")





#region persona - function based views
def persona_list(request):
    form, queryset = SearchForm(request.GET), None
    if form.is_valid():
        cd = form.cleaned_data
        if not cd['q']:
            queryset = Persona.objects.all()
        else:
            queryset = Persona.objects.filter(
                Q(nombre__icontains=cd['q'])    |
                Q(apellidos__icontains=cd['q'])
            )
    return render(request, "adopcion__persona_listado.html", {
        "code": "fnc/",
        "buscador": form,
        "object_list": queryset,
    })


def persona_form(request, _id=None):
    # Se verifica la existencia
    instance = get_object_or_404(Persona, id=_id) if _id else None
    # Update/create
    if request.method == "POST":
        form = PersonaForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success( request,
                'Se {} correctamente la persona <strong>{} {}</strong>'.format(
                    "modifico" if instance else "agrego",
                    instance.nombre if instance else form.cleaned_data.get('nombre'),
                    instance.apellidos if instance else form.cleaned_data.get('apellidos'),
                )
            )
            return HttpResponseRedirect( reverse('persona_list') )
    else:
        form = PersonaForm(instance=instance) if instance else PersonaForm()
    return render(request, "adopcion__persona_form.html", { "form": form })


def persona_delete(request, _id):
    instance = get_object_or_404(Persona, id=_id)
    return generic_delete(
        request=request,
        instance=instance,
        tpl_name="adopcion__persona_delete.html",
        redirect=reverse('persona_list'),
        success_message="Se elimino el registro de: <strong>{} {}</strong>".format(instance.nombre, instance.apellidos)
    )
#endregion






#region persona - class based views
class PersonaListView(ListView):
    model = Persona
    template_name = "adopcion__persona_listado.html"
    form_class = SearchForm

    
    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            return self.model.objects.filter(Q(nombre__icontains=cd['q']) | Q(apellidos__icontains=cd['q']))
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PersonaListView, self).get_context_data(**kwargs)
        context['buscador'] = self.form_class()
        return context

    

class PersonaCreateView(SuccessMessageMixin, CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = "adopcion__persona_form.html"
    success_url = reverse_lazy("persona_list_cbv")
    success_message = "Se agrego correctamente la persona <strong>%(nombre)s %(apellidos)s</strong>"



class PersonaUpdateView(SuccessMessageMixin, UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = "adopcion__persona_form.html"
    success_url = reverse_lazy("persona_list_cbv")
    success_message = "Se modifico correctamente la persona <strong>%(nombre)s %(apellidos)s</strong>"



class PersonaDeleteView(SuccessMessageMixin, DeleteView):
    model = Persona
    form_class = PersonaForm
    template_name = "adopcion__persona_delete.html"
    success_url = reverse_lazy("persona_list_cbv")
    success_message = "Se elimino correctamente la persona <strong>%(nombre)s %(apellidos)s</strong>"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(PersonaDeleteView, self).delete(request, *args, **kwargs)
#endregion


# region persona - API Clase based views
class PersonaApiListView(ListView):
    endpoint = 'http://localhost:8000/api/persona/'
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
        context['code'] = "api/",
        context['buscador'] = self.form_class()
        return context

    def get_endpoint(self, search_query=None):
        if search_query:
            self.endpoint = "{endpoint}?q={q}".format(endpoint=self.endpoint, q=search_query)
        return self.endpoint

    def get_info_via_api(self, search_query=None):
        data = []
        try:
            response = requests.get(self.get_endpoint(search_query))
            data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return data


def persona_form_api(request, _id=None):
    initial = {}
    # Se verifica la existencia
    if _id:
        try:
            response = requests.get('http://localhost:8000/api/persona/{id}'.format(id=_id))
            if response.status_code != 200:
                raise Http404
            initial = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            messages.error(request, 'Un error a ocurrido consultando los datos de la persona con id: {id}'
                                    ''.format(id=_id))
            return HttpResponseRedirect(reverse('persona_list_api'))

    form = PersonaForm(initial=initial) if initial else PersonaForm()

    # Update/create
    if request.method == "POST":
        form = PersonaForm(request.POST, initial=initial)
        if form.is_valid():
            api_error = False
            try:
                if initial:
                    response = requests.put('http://localhost:8000/api/persona/{id}/'.format(id=_id),
                                            data=form.cleaned_data)
                else:
                    # TODO: Crear persona
                    pass

                # Se verifica si la api pudo actualizar los datos de la persona
                if not response or response.status_code != 200:
                    api_error = True
                    messages.error(request, 'Un error ha ocurrido intentando aplicar la accion sobre la persona '
                                            '<strong>{first_name} {last_name}</strong>'
                                            ''.format(first_name=form.cleaned_data.get('nombre'),
                                                      last_name=form.cleaned_data.get('apellidos')))

            except (ConnectionError, ConnectTimeout) as err:
                api_error = True
                messages.error(request, 'Un error desconocido ha ocurrido intentando aplicar la accion sobre la '
                                        'persona <strong>{first_name} {last_name}</strong>'
                                        ''.format(first_name=form.cleaned_data.get('nombre'),
                                                  last_name=form.cleaned_data.get('apellidos')))

            # Si no ocurrio ningun error durante el intento de crear o eliminar, se manda el mensaje de exito
            if not api_error:
                messages.success(request, 'Se ha realizado con exito la accion sobre la persona '
                                          '<strong>{first_name} {last_name}</strong>'
                                          ''.format(first_name=form.cleaned_data.get('nombre'),
                                                    last_name=form.cleaned_data.get('apellidos')))
            return HttpResponseRedirect(reverse('persona_list_api'))

    return render(request, "adopcion__persona_form.html", {
        "form": form,
    })
# endregion

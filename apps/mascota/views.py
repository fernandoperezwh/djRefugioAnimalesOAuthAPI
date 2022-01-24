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
from apps.mascota.models import Vacuna, Mascota
from apps.mascota.forms import VacunaForm, MascotaForm
from djRefugioAnimales.forms import SearchForm
from djRefugioAnimales.utils import generic_delete, generic_api_delete


# Create your views here.
def mascotas_index(request):
    return HttpResponse("Hello world")


#region Vacuna - function based views
def vacuna_list(request):
    form, queryset = SearchForm(request.GET), None
    if form.is_valid():
        cd = form.cleaned_data
        if not cd['q']:
            queryset = Vacuna.objects.all()
        else:
            queryset = Vacuna.objects.filter(nombre__icontains=cd['q'])
    return render(request, "mascota__vacuna_listado.html", {
        'create_url': 'vacuna_new_fnc',
        'edit_url': 'persona_edit_fnc',
        'delete_url': 'persona_delete_fnc',
        "buscador": form,
        "object_list": queryset,
    })


def vacuna_form(request, _id=None):
    instance = get_object_or_404(Vacuna, id=_id) if _id else None
    # Update/create
    if request.method == "POST":
        form = VacunaForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success( request,
                'Se {} correctamente la vacuna <strong>{}</strong>'.format(
                    "modifico" if instance else "agrego",
                    instance.nombre if instance else form.cleaned_data.get('nombre'),
                )
            )
            return HttpResponseRedirect(reverse('vacuna_list_fnc'))
    else:
        form = VacunaForm(instance=instance) if instance else VacunaForm()
    return render(request, "mascota__vacuna_form.html", { "form":   form })


def vacuna_delete(request, _id):
    instance = get_object_or_404(Vacuna, id=_id)
    return generic_delete(
        request=request,
        instance=instance,
        tpl_name="mascota__vacuna_delete.html",
        redirect=reverse('vacuna_list_fnc'),
        success_message="Se elimino el registro de la vacuna: <strong>{}</strong>".format(instance.nombre)
    )
#endregion


#region Vacuna - class based views
class VacunaListView(ListView):
    model = Vacuna
    template_name = "mascota__vacuna_listado.html"
    form_class = SearchForm

    
    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            return self.model.objects.filter(nombre__icontains=cd['q'])
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(VacunaListView, self).get_context_data(**kwargs)
        context['buscador'] = self.form_class()
        context['create_url'] = 'vacuna_new_cbv'
        context['edit_url'] = 'vacuna_edit_cbv'
        context['delete_url'] = 'vacuna_delete_cbv'
        return context


class VacunaCreateView(SuccessMessageMixin, CreateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = "mascota__vacuna_form.html"
    success_url = reverse_lazy("vacuna_list_cbv")
    success_message = "Se agrego correctamente la vacuna <strong>%(nombre)s</strong>"


class VacunaUpdateView(SuccessMessageMixin, UpdateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = "mascota__vacuna_form.html"
    success_url = reverse_lazy("vacuna_list_cbv")
    success_message = "Se modifico correctamente la vacuna <strong>%(nombre)s</strong>"


class VacunaDeleteView(SuccessMessageMixin, DeleteView):
    model = Vacuna
    form_class = VacunaForm
    template_name = "mascota__vacuna_delete.html"
    success_url = reverse_lazy("vacuna_list_cbv")
    success_message = "Se elimino correctamente la vacuna <strong>%(nombre)s</strong>"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(VacunaDeleteView, self).delete(request, *args, **kwargs)
#endregion


# region Vacuna - api views
class VacunaApiListView(ListView):
    endpoint = 'http://localhost:8000/api/vacuna/'
    model = Vacuna
    template_name = "mascota__vacuna_listado.html"
    form_class = SearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        cd = dict()
        if form.is_valid():
            cd = form.cleaned_data
        return self.get_info_via_api(cd.get('q'))

    def get_context_data(self, **kwargs):
        context = super(VacunaApiListView, self).get_context_data(**kwargs)
        context['create_url'] = 'vacuna_new_api'
        context['edit_url'] = 'vacuna_edit_api'
        context['delete_url'] = 'vacuna_delete_api'
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


def vacuna_form_api(request, _id=None):
    RETURN_URL = 'vacuna_list_api'
    initial = {}
    # Se verifica la existencia
    if _id:
        try:
            response = requests.get('http://localhost:8000/api/vacuna/{id}'.format(id=_id))
            if response.status_code != 200:
                raise Http404
            initial = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            messages.error(request, 'Un error a ocurrido consultando los datos de la vacuna con id: {id}'
                                    ''.format(id=_id))
            return HttpResponseRedirect(reverse('vacuna_list_api'))

    form = VacunaForm(initial=initial) if initial else VacunaForm()

    # Update/create
    if request.method == "POST":
        form = VacunaForm(request.POST, initial=initial)
        if form.is_valid():
            try:
                if initial:
                    # Editar registro de una vacuna
                    response = requests.put('http://localhost:8000/api/vacuna/{id}/'.format(id=_id),
                                            data=form.cleaned_data)
                else:
                    # Crear registro de una vacuna
                    response = requests.post('http://localhost:8000/api/vacuna/', data=form.cleaned_data)

            except (ConnectionError, ConnectTimeout) as err:
                messages.error(request, 'Un error desconocido ha ocurrido intentando aplicar la accion sobre la '
                                        'vacuna <strong>{name}</strong>'
                                        ''.format(name=form.cleaned_data.get('nombre')))
                return HttpResponseRedirect(reverse(RETURN_URL))

            # Se verifica si la api pudo actualizar/crear los datos de la vacuna
            if response.status_code not in (200, 201):
                messages.error(request, 'Un error ha ocurrido intentando aplicar la accion sobre la vacuna '
                                        '<strong>{name}</strong>'
                                        ''.format(name=form.cleaned_data.get('nombre')))
                return HttpResponseRedirect(reverse(RETURN_URL))
            # Si no ocurrio ningun error durante el intento de crear o eliminar, se manda el mensaje de exito
            messages.success(request, 'Se ha realizado con exito la accion sobre la vacuna <strong>{name}</strong>'
                                      ''.format(name=form.cleaned_data.get('nombre')))
            return HttpResponseRedirect(reverse(RETURN_URL))

    return render(request, "mascota__vacuna_form.html", {
        "form": form,
    })


def vacuna_delete_api(request, _id):
    RETURN_URL = 'vacuna_list_api'
    ENDPOINT = 'http://localhost:8000/api/vacuna/{id}'.format(id=_id)
    # Se intenta obtener el registro a eliminar
    try:
        response = requests.get(ENDPOINT.format(id=_id))
        if response.status_code != 200:
            raise Http404
        instance = response.json()
    except (ConnectionError, ConnectTimeout) as err:
        messages.error(request, 'Un error a ocurrido consultando los datos de la vacuna con id: {id}'
                                ''.format(id=_id))
        return HttpResponseRedirect(reverse(RETURN_URL))
    # Se manda a llamar las instrucciones genericas para eliminar en base al funcionamiento del api
    return generic_api_delete(
        request=request,
        endpoint=ENDPOINT,
        instance=instance,
        tpl_name="mascota__vacuna_delete.html",
        redirect=reverse(RETURN_URL),
        custom_messages={
            'success': 'Se elimino el registro de: <strong>{}</strong>'.format(instance.get('nombre')),
            'error': 'Un error ha ocurrido intentando eliminar el registro de: <strong>{}</strong>'
                     ''.format(instance.get('nombre')),
        }
    )
# endregion


#region Mascota - function based views
def mascota_list(request):
    form, queryset = SearchForm(request.GET), None
    if form.is_valid():
        cd = form.cleaned_data
        if not cd['q']:
            queryset = Mascota.objects.all()
        else:
            queryset = Mascota.objects.filter(
                Q(nombre__icontains=cd['q'])             |
                Q(persona__nombre__icontains=cd['q'])    |
                Q(persona__apellidos__icontains=cd['q'])
            )
    return render(request, "mascota__mascota_listado.html", {
        'edit_url': 'mascota_edit_fnc',
        'delete_url': 'mascota_delete_fnc',
        "buscador": form,
        "object_list": queryset,
    })


def mascota_form(request, _id=None):
    instance = get_object_or_404(Mascota, id=_id) if _id else None
    # Update/create
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success( request,
                'Se {} correctamente la mascota <strong>{}</strong>'.format(
                    "modifico" if instance else "agrego",
                    instance.nombre if instance else form.cleaned_data.get('nombre'),
                )
            )
            return HttpResponseRedirect(reverse('mascota_list_fnc'))
    else:
        form = MascotaForm(instance=instance) if instance else MascotaForm()
    return render(request, "mascota__mascota_form.html", { "form":   form })


def mascota_delete(request, _id):
    instance = get_object_or_404(Mascota, id=_id)
    return generic_delete(
        request=request,
        instance=instance,
        tpl_name="mascota__mascota_delete.html",
        redirect=reverse('mascota_list_fnc'),
        success_message="Se elimino el registro de la mascota: <strong>{}</strong>".format(instance.nombre)
    )
#endregion


#region Mascota - class based views
class MascotaListView(ListView):
    model = Mascota
    template_name = "mascota__mascota_listado.html"
    form_class = SearchForm

    
    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            return self.model.objects.filter(
                Q(nombre__icontains=cd['q'])             |
                Q(persona__nombre__icontains=cd['q'])    |
                Q(persona__apellidos__icontains=cd['q'])
            )
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MascotaListView, self).get_context_data(**kwargs)
        context['buscador'] = self.form_class()
        context['edit_url'] = 'mascota_edit_cbv'
        context['delete_url'] = 'mascota_delete_cbv'
        return context


class MascotaCreateView(SuccessMessageMixin, CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota__mascota_form.html"
    success_url = reverse_lazy("mascota_list_cbv")
    success_message = "Se agrego correctamente la mascota <strong>%(nombre)s</strong>"


class MascotaUpdateView(SuccessMessageMixin, UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota__mascota_form.html"
    success_url = reverse_lazy("mascota_list_cbv")
    success_message = "Se modifico correctamente la mascota <strong>%(nombre)s</strong>"


class MascotaDeleteView(SuccessMessageMixin, DeleteView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota__mascota_delete.html"
    success_url = reverse_lazy("mascota_list_cbv")
    success_message = "Se elimino correctamente la mascota <strong>%(nombre)s</strong>"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(MascotaDeleteView, self).delete(request, *args, **kwargs)
#endregion

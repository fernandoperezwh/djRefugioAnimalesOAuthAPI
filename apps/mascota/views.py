from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# local imports
from apps.mascota.models import Vacuna, Mascota
from apps.mascota.forms import VacunaForm, MascotaForm
from djRefugioAnimales.forms import SearchForm
from djRefugioAnimales.utils import generic_delete

# Create your views here.
def mascotas_index(request):
    return HttpResponse("Hello world")


"""
    Vacunas
"""
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
        "code": "fnc/",
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
            return HttpResponseRedirect( reverse('vacuna_list') )
    else:
        form = VacunaForm(instance=instance) if instance else VacunaForm()
    return render(request, "mascota__vacuna_form.html", { "form":   form })


def vacuna_delete(request, _id):
    instance = get_object_or_404(Vacuna, id=_id)
    return generic_delete(
        request=request,
        instance=instance,
        tpl_name="mascota__vacuna_delete.html",
        redirect=reverse('vacuna_list'),
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




"""
    Mascotas
"""
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
        "code": "fnc/",
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
            return HttpResponseRedirect( reverse('mascota_list') )
    else:
        form = MascotaForm(instance=instance) if instance else MascotaForm()
    return render(request, "mascota__mascota_form.html", { "form":   form })


def mascota_delete(request, _id):
    instance = get_object_or_404(Mascota, id=_id)
    return generic_delete(
        request=request,
        instance=instance,
        tpl_name="mascota__mascota_delete.html",
        redirect=reverse('mascota_list'),
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

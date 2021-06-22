from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

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
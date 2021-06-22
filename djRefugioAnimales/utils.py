from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect


def build_form_input_attrs(key):
    return {
        "id":               key,
        "aria-describedby": "{}_errors".format(key),
        "class":            "form-control",
    }




def generic_delete(request, instance, tpl_name, redirect, success_message=None):
    DEFAULT_SUCCESS_MESSAGE = "Se elimino el registro correctamente."
    if request.method == "POST":
        instance.delete()
        messages.success(request, success_message or DEFAULT_SUCCESS_MESSAGE)
        return HttpResponseRedirect( redirect )
    return render(request, tpl_name, { "object": instance })
    
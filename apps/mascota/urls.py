from django.conf.urls import url
# local imports
from apps.mascota import views

urlpatterns = [
    url(r'^vacuna/api/list/$', views.VacunaApiListView.as_view(), name="vacuna_list_api"),
    url(r'^vacuna/api/new/$', views.vacuna_form_api, name="vacuna_new_api"),
    url(r'^vacuna/api/edit/(\d+)/$', views.vacuna_form_api, name="vacuna_edit_api"),
    url(r'^vacuna/api/delete/(\d+)/$', views.vacuna_delete_api, name="vacuna_delete_api"),
]
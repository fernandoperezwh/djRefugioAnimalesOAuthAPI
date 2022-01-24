from django.conf.urls import url
# local imports
from apps.mascota import views

urlpatterns = [
    url(r'^$', views.mascotas_index),

    #region Vacunas - function based views
    url(r'^vacuna/fnc/list/$', views.vacuna_list, name="vacuna_list_fnc"),
    url(r'^vacuna/fnc/new/$', views.vacuna_form, name="vacuna_new_fnc"),
    url(r'^vacuna/fnc/edit/(\d+)/$', views.vacuna_form, name="vacuna_edit_fnc"),
    url(r'^vacuna/fnc/delete/(\d+)/$', views.vacuna_delete, name="vacuna_delete_fnc"),
    #endregion
    #region Vacunas - class based views
    url(r'^vacuna/list/$', views.VacunaListView.as_view(), name="vacuna_list_cbv"),
    url(r'^vacuna/new/$', views.VacunaCreateView.as_view(), name="vacuna_new_cbv"),
    url(r'^vacuna/edit/(?P<pk>[0-9]+)/$', views.VacunaUpdateView.as_view(), name="vacuna_edit_cbv"),
    url(r'^vacuna/delete/(?P<pk>[0-9]+)/$', views.VacunaDeleteView.as_view(), name="vacuna_delete_cbv"),
    #endregion
    #region Vacunas - api views
    url(r'^vacuna/api/list/$', views.VacunaApiListView.as_view(), name="vacuna_list_api"),
    url(r'^vacuna/api/new/$', views.vacuna_form_api, name="vacuna_new_api"),
    url(r'^vacuna/api/edit/(\d+)/$', views.vacuna_form_api, name="vacuna_edit_api"),
    url(r'^vacuna/api/delete/(\d+)/$', views.vacuna_delete_api, name="vacuna_delete_api"),
    #endregion




    #region Mascotas - function based views
    url(r'^mascota/fnc/list/$', views.mascota_list, name="mascota_list_fnc"),
    url(r'^mascota/fnc/new/$', views.mascota_form, name="mascota_new_fnc"),
    url(r'^mascota/fnc/edit/(\d+)/$', views.mascota_form, name="mascota_edit_fnc"),
    url(r'^mascota/fnc/delete/(\d+)/$', views.mascota_delete, name="mascota_delete_fnc"),
    #endregion
    #region Mascotas - class based views
    url(r'^mascota/list/$', views.MascotaListView.as_view(), name="mascota_list_cbv"),
    url(r'^mascota/new/$', views.MascotaCreateView.as_view(), name="mascota_new_cbv"),
    url(r'^mascota/edit/(?P<pk>[0-9]+)/$', views.MascotaUpdateView.as_view(), name="mascota_edit_cbv"),
    url(r'^mascota/delete/(?P<pk>[0-9]+)/$', views.MascotaDeleteView.as_view(), name="mascota_delete_cbv"),
    #endregion
    #region Mascotas - api views
    url(r'^mascota/api/list/$', views.mascota_list, name="mascota_list_api"),
    url(r'^mascota/api/new/$', views.mascota_form, name="mascota_new_api"),
    url(r'^mascota/api/edit/(\d+)/$', views.mascota_form, name="mascota_edit_api"),
    url(r'^mascota/api/delete/(\d+)/$', views.mascota_delete, name="mascota_delete_api"),
    #endregion
]
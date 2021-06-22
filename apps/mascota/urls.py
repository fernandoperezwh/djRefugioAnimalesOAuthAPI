from django.conf.urls import url
# local imports
from apps.mascota import views

urlpatterns = [
    url(r'^$', views.mascotas_index),

    #region Vacunas - function based views
    url(r'^vacuna/fnc/list/$', views.vacuna_list, name="vacuna_list"),
    url(r'^vacuna/fnc/new/$', views.vacuna_form),
    url(r'^vacuna/fnc/edit/(\d+)/$', views.vacuna_form),
    url(r'^vacuna/fnc/delete/(\d+)/$', views.vacuna_delete),
    #region Vacunas - class based views
    url(r'^vacuna/list/$', views.VacunaListView.as_view(), name="vacuna_list_cbv"),
    url(r'^vacuna/new/$', views.VacunaCreateView.as_view()),
    url(r'^vacuna/edit/(?P<pk>[0-9]+)/$', views.VacunaUpdateView.as_view()),
    url(r'^vacuna/delete/(?P<pk>[0-9]+)/$', views.VacunaDeleteView.as_view()),
    #endregion




    #region Mascotas - function based views
    url(r'^mascota/fnc/list/$', views.mascota_list, name="mascota_list"),
    url(r'^mascota/fnc/new/$', views.mascota_form),
    url(r'^mascota/fnc/edit/(\d+)/$', views.mascota_form),
    url(r'^mascota/fnc/delete/(\d+)/$', views.mascota_delete),
    #region Mascotas - class based views
    url(r'^mascota/list/$', views.MascotaListView.as_view(), name="mascota_list_cbv"),
    url(r'^mascota/new/$', views.MascotaCreateView.as_view()),
    url(r'^mascota/edit/(?P<pk>[0-9]+)/$', views.MascotaUpdateView.as_view()),
    url(r'^mascota/delete/(?P<pk>[0-9]+)/$', views.MascotaDeleteView.as_view()),
    #endregion
]
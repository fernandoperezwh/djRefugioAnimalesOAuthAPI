# Django packages
from django.conf.urls import url
# local packages
from apps.api import views

urlpatterns = [
    # region endpoints persona
    url(r'^persona/$', views.PersonaList.as_view()),
    url(r'^persona/(?P<pk>\d+)/$', views.PersonaDetail.as_view()),
    # endregion
    # region endpoints vacuna
    url(r'^vacuna/$', views.VacunaList.as_view()),
    url(r'^vacuna/(?P<pk>\d+)/$', views.VacunaDetail.as_view()),
    # enregion
    # region endpoints mascota
    url(r'^mascota/$', views.MascotaList.as_view()),
    url(r'^mascota/(?P<pk>\d+)/$', views.MascotaDetail.as_view()),
    # endregion


    # region protected resources - persona
    url(r'^priv/persona/$', views.PersonaPrivateList.as_view()),
    url(r'^priv/persona/(?P<pk>\d+)/$', views.PersonaPrivateDetail.as_view()),
    # endregion
    # region endpoints vacuna
    url(r'^priv/vacuna/$', views.VacunaPrivateList.as_view()),
    url(r'^priv/vacuna/(?P<pk>\d+)/$', views.VacunaPrivateDetail.as_view()),
    # enregion
    # region endpoints mascota
    url(r'^priv/mascota/$', views.MascotaPrivateList.as_view()),
    url(r'^priv/mascota/(?P<pk>\d+)/$', views.MascotaPrivateDetail.as_view()),
    # endregion
]

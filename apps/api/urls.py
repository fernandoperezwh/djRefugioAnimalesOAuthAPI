# Django packages
from django.conf.urls import url
# local packages
from apps.api import views

urlpatterns = [
    # endpoints persona
    url(r'^persona/$', views.PersonaList.as_view()),
    url(r'^persona/(?P<pk>\d+)/$', views.PersonaDetail.as_view()),

    # endpoints vacuna
    url(r'^vacuna/$', views.VacunaList.as_view()),
    url(r'^vacuna/(?P<pk>\d+)/$', views.VacunaDetail.as_view()),

    # endpoints mascota
]

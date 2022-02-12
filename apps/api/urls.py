# Django packages
from django.conf.urls import url
# local packages
from apps.api import views

urlpatterns = [
    url(r'^persona/$', views.PersonaList.as_view()),
    url(r'^persona/(?P<pk>\d+)/$', views.PersonaDetail.as_view()),
    url(r'^vacuna/$', views.VacunaList.as_view()),
    url(r'^vacuna/(?P<pk>\d+)/$', views.VacunaDetail.as_view()),
    url(r'^mascota/$', views.MascotaList.as_view()),
    url(r'^mascota/(?P<pk>\d+)/$', views.MascotaDetail.as_view()),
]

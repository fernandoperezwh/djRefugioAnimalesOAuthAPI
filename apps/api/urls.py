# Django packages
from django.conf.urls import url
# local packages
from apps.api import views

urlpatterns = [
    url(r'^persona/$', views.PersonaList.as_view()),
    url(r'^persona/(?P<pk>\d+)/$', views.PersonaDetail.as_view()),
]

from django.conf.urls import url
# local imports
from apps.adopcion import views


urlpatterns = [
    url(r'^$', views.adopcion_index),

    # region Personas - function based views
    url(r'^persona/fnc/list/$', views.persona_list, name="persona_list"),
    url(r'^persona/fnc/new/$', views.persona_form),
    url(r'^persona/fnc/edit/(\d+)/$', views.persona_form),
    url(r'^persona/fnc/delete/(\d+)/$', views.persona_delete),
    # endregion

    # region Personas - class based views
    url(r'^persona/list/$', views.PersonaListView.as_view(), name="persona_list_cbv"),
    url(r'^persona/new/$', views.PersonaCreateView.as_view()),
    url(r'^persona/edit/(?P<pk>[0-9]+)/$', views.PersonaUpdateView.as_view()),
    url(r'^persona/delete/(?P<pk>[0-9]+)/$', views.PersonaDeleteView.as_view()),
    # endregion

    # region Personas - api class based views
    url(r'^persona/api/list/$', views.PersonaApiListView.as_view(), name="persona_list_api"),
    url(r'^persona/api/new/$', views.persona_form),
    url(r'^persona/api/edit/(\d+)/$', views.persona_form_api),
    # endregion
]
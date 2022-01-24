from django.conf.urls import url
# local imports
from apps.adopcion import views


urlpatterns = [
    url(r'^$', views.adopcion_index),

    # region Personas - function based views
    url(r'^persona/fnc/list/$', views.persona_list, name='persona_list_fnc'),
    url(r'^persona/fnc/new/$', views.persona_form, name='persona_new_fnc'),
    url(r'^persona/fnc/edit/(\d+)/$', views.persona_form, name='persona_edit_fnc'),
    url(r'^persona/fnc/delete/(\d+)/$', views.persona_delete, name='persona_delete_fnc'),
    # endregion

    # region Personas - class based views
    url(r'^persona/list/$', views.PersonaListView.as_view(), name='persona_list_cbv'),
    url(r'^persona/new/$', views.PersonaCreateView.as_view(), name='persona_new_cbv'),
    url(r'^persona/edit/(?P<pk>[0-9]+)/$', views.PersonaUpdateView.as_view(), name='persona_edit_cbv'),
    url(r'^persona/delete/(?P<pk>[0-9]+)/$', views.PersonaDeleteView.as_view(), name='persona_delete_cbv'),
    # endregion

    # region Personas - api views
    url(r'^persona/api/list/$', views.PersonaApiListView.as_view(), name='persona_list_api'),
    url(r'^persona/api/new/$', views.persona_form_api, name='persona_new_api'),
    url(r'^persona/api/edit/(\d+)/$', views.persona_form_api, name='persona_edit_api'),
    url(r'^persona/api/delete/(\d+)/$', views.persona_delete_api, name='persona_delete_api'),
    # endregion
]
from django.conf.urls import url
# local imports
from apps.adopcion import views


urlpatterns = [
    url(r'^persona/api/list/$', views.PersonaApiListView.as_view(), name='persona_list_api'),
    url(r'^persona/api/new/$', views.persona_form_api, name='persona_new_api'),
    url(r'^persona/api/edit/(\d+)/$', views.persona_form_api, name='persona_edit_api'),
    url(r'^persona/api/delete/(\d+)/$', views.persona_delete_api, name='persona_delete_api'),
]
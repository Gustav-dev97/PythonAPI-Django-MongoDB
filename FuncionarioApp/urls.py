from django.urls import re_path as url
from FuncionarioApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^departamento$',views.departamentoApi),
    url(r'^departamento/([0-9]+)$', views.departamentoApi),

    url(r'^funcionario$',views.funcionarioApi),
    url(r'^funcionario/([0-9]+)$', views.funcionarioApi),

    url(r'^funcionario/salvararquivo', views.salvarArquivo)
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
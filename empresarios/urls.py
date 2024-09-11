from django.urls import path
from .views import cadastrar_empresa, listar_empresas, empresa, add_doc, excluir_doc, add_metrica, gerenciar_proposta, dashboard

urlpatterns = [
    path('cadastrar_empresa/', cadastrar_empresa, name="cadastrar_empresa"),
    path('listar_empresas/', listar_empresas, name='listar_empresas'),
    path('empresa/<int:id>', empresa, name='empresa'),
    path('add_doc/<int:id>', add_doc, name='add_doc'),
    path('excluir_doc/<int:id>', excluir_doc, name='excluir_doc'),
    path('add_metrica/<int:id>', add_metrica, name="add_metrica"),
    path('gerenciar_proposta/<int:id>', gerenciar_proposta, name="gerenciar_proposta"),
    path('dashboard/<int:id>', dashboard, name="dashboard"),
]

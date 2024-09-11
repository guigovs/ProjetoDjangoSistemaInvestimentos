from django.urls import path
from .views import sugestao, ver_empresa, realizar_proposta, assinar_contrato

urlpatterns = [
    path('sugestao/', sugestao, name="sugestao"),
    path('ver_empresa/<int:id>', ver_empresa, name='ver_empresa'),
    path('realizar_proposta/<int:id>', realizar_proposta, name='realizar_proposta'),
    path('assinar_contrato/<int:id>', assinar_contrato, name="assinar_contrato"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('cadastrar_remessa/', views.cadastrar_remessa, name='cadastrar_remessa'),
    path('cadastrar_remessa/xml/', views.abrir_xml_remessa, name='abrir_xml_remessa'),
    path('cadastrar_retorno/retornar_remessa/', views.retornar_remessa, name='retornar_remessa'),
    path('cadastrar_retorno/<int:nfe>/', views.cadastrar_retorno, name='cadastrar_retorno'),
    path('cadastrar_retorno/<int:nfe>/xml', views.abrir_xml_retorno, name='abrir_xml_retorno'),
]

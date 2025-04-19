from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static
app_name = "Biens"


urlpatterns = [
      path('', Affichage.as_view(), name='biens'),
      path('ajout/', AjoutBiens.as_view(), name='ajout'),
      path('delete/<int:pk>/', delete.as_view(), name='delete'),
      path('supprimer/<int:pk>/', Supprimer.as_view(), name='supprimer'),
      path('modication/<int:pk>/', update_donnees.as_view(), name='modifier'),
      path('detail/<int:pk>/', edit.as_view(), name='detail'),
      path('corbeille/', CorbeilleListView.as_view(), name='corbeille'),
      path("restaurer/<int:biens_id>/", restaurer_bien, name="restaurer_bien"),
      path('recherche/', recherche, name='recherche'),
      path('telecharger/<int:biens_id>/', telecharger_document, name='telecharger_document'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



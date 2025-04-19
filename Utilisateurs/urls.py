from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('', LocationListView.as_view(),name='acc'),
    path('utilisateur/', Affichage.as_view(), name='home'),
    path('accounts/login/',Connecter_compte, name= 'acount_login'),
    # path('connecter/',Connecter_compte, name= 'login'),
    path('creation/',Creation_compte, name= 'creation'),
    path('deconnection/', Deconnection, name="deconnection"),
    path('api/online-users/', online_users, name='online_users'),
    path('toggle-user/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path("permissions/<int:user_id>/", permissions, name="permission_page"),
   

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
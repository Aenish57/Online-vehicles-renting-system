from django.urls import path
from . import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload_vehicle/', views.upload_vehicle,name="upload_vehicle"),
    path('Owner/',include("Owner.urls")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)
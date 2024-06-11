from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
# maps/urls.py
from .views import GeocodeView
from .views import GeocodeView, ReverseGeocodeView



urlpatterns = [
    path('',views.getRoutes),
    path('places/', views.getPlaces),
    path('places/create', views.createPlace),
    path('geocode/', GeocodeView.as_view(), name='geocode'),
    path('reverse-geocode/', ReverseGeocodeView.as_view(), name='reverse-geocode'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
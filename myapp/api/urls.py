from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import GeocodeView, ReverseGeocodeView, SignupView, LoginView, createPlace, tourView, getPlaces


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('create_place/', createPlace, name='create_place'),  
    path('places/', getPlaces, name='get_places'),
    path('geocode/', GeocodeView.as_view(), name='geocode'),
    path('reverse-geocode/', ReverseGeocodeView.as_view(), name='reverse-geocode'),
    path('tour/', tourView.as_view(), name='create_tour'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
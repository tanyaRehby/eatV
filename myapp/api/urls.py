from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings
from .views import GeocodeView, ReverseGeocodeView, SignupView, LoginView, createPlace, tourView, CreatePlaceView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    #path('password_reset/', views.password_reset_view, name='password_reset'),
    path('create_place/', CreatePlaceView.as_view(), name='create_place'),

    path('places/', views.getPlaces),
    path('geocode/', GeocodeView.as_view(), name='geocode'),
    path('reverse-geocode/', ReverseGeocodeView.as_view(), name='reverse-geocode'),
    path('tour/', tourView.as_view(), name='create_tour'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
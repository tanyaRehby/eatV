from django.urls import path
from . import views 

urlpatterns = [
    path('',views.getRoutes),
    path('journeys/', views.getJourneys),
    # path('journeys/<str:pk>', views.getJourney),

]
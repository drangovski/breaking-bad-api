from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # Characters
    path('api/characters/', views.CharacterList.as_view(), name="all_characters"),
    path('api/characters/<int:pk>', views.CharacterDetail.as_view(), name="get_character"),

    # Locations
    path('api/locations/', views.LocationList.as_view(), name="all_locations"),
    path('api/locations/<int:pk>', views.LocationDetail.as_view(), name="get_location"),
]

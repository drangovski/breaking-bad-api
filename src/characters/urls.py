from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('api/', views.api_overview, name="api_overview"),
    path('api/characters/', views.CharacterList.as_view(), name="all_characters"),
    path('api/characters/<int:pk>', views.CharacterDetail.as_view(), name="get_character"),

]

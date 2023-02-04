from django.urls import path

from . import views

urlpatterns = [
    # API ENDPOINTS
    path('api/characters/', views.all_characters, name="all_characters"),
    path('api/characters/<int:id>', views.get_character, name="get_character"),
]

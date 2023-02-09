from django.urls import path


from . import views

urlpatterns = [
    path('api/locations/', views.LocationList.as_view(), name="all_locations"),
    path('api/locations/<int:pk>', views.LocationDetail.as_view(), name="get_location"),
]

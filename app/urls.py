from django.urls import path

from .views import SpotListView, CoordsEditor

app_name = "app"

urlpatterns = [
    path('spot-list/', SpotListView.as_view(), name='spot-list'),
    path('edit-coords/<int:pk>', CoordsEditor.as_view(), name='edit-coords'),
]

from django.urls import path
from .views import (
    HabitListCreateView,
    HabitRetrieveUpdateDestroyView,
    PublicHabitListView,
)

urlpatterns = [
    path('my-habits/', HabitListCreateView.as_view(), name='my-habit-list-create'),
    path('my-habits/<int:pk>/', HabitRetrieveUpdateDestroyView.as_view(), name='my-habit-retrieve-update-destroy'),
    path('public-habits/', PublicHabitListView.as_view(), name='public-habit-list'),
]

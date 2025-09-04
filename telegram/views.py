from rest_framework import generics
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    # permission_classes = [IsAuthenticated, IsOwner] # Временно закомментировано для отладки

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)

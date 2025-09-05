from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Habit
import datetime


class HabitApiTestCase(APITestCase):
    def setUp(self):
        # Создаем двух пользователей
        self.user1 = User.objects.create_user(
            username='user1', password='testpassword123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='testpassword123'
        )

        # Аутентифицируем первого пользователя
        self.client.force_authenticate(user=self.user1)

        # Создаем привычку для первого пользователя
        self.habit1 = Habit.objects.create(
            user=self.user1,
            place='Дома',
            time=datetime.time(8, 0),
            action='Делать зарядку',
            estimated_time=120,  # <-- Сохраняем как integer (секунды)
            is_public=True
        )

        # Создаем привычку для второго пользователя
        self.habit2 = Habit.objects.create(
            user=self.user2,
            place='На работе',
            time=datetime.time(10, 0),
            action='Пить воду',
            estimated_time=60,
            is_public=False
        )

    def test_create_habit(self):
        """Тест создания привычки."""
        url = reverse('my-habit-list-create')
        data = {
            "place": "В парке",
            "time": "07:00:00",
            "action": "Бегать",
            "estimated_time": 120,  # <-- ИСПРАВЛЕННЫЕ ДАННЫЕ
            "frequency": 2,
            "is_public": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(Habit.objects.latest('id').action, 'Бегать')

    def test_list_my_habits(self):
        """Тест просмотра списка своих привычек."""
        url = reverse('my-habit-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Убеждаемся, что user1 видит только свою привычку
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['action'], self.habit1.action
        )

    def test_retrieve_own_habit(self):
        """Тест просмотра своей привычки."""
        url = reverse(
            'my-habit-retrieve-update-destroy', args=[self.habit1.pk]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], self.habit1.action)

    def test_retrieve_foreign_habit_forbidden(self):
        """Тест: пользователь не может просматривать чужую привычку."""
        url = reverse(
            'my-habit-retrieve-update-destroy', args=[self.habit2.pk]
        )
        response = self.client.get(url)
        # Ожидаем 404, так как пермишн IsOwner не найдет объект
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_habit(self):
        """Тест обновления своей привычки."""
        url = reverse(
            'my-habit-retrieve-update-destroy', args=[self.habit1.pk]
        )
        data = {
            'action': 'Делать утреннюю гимнастику',
            "estimated_time": 180
        }  # <--- ИСПРАВЛЕННЫЕ ДАННЫЕ
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit1.refresh_from_db()
        self.assertEqual(self.habit1.action, 'Делать утреннюю гимнастику')
        self.assertEqual(self.habit1.estimated_time, 180)

    def test_update_foreign_habit_forbidden(self):
        """Тест: пользователь не может обновлять чужую привычку."""
        url = reverse(
            'my-habit-retrieve-update-destroy', args=[self.habit2.pk]
        )
        data = {'action': 'Попытка взлома'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_habit(self):
        """Тест удаления своей привычки."""
        url = reverse(
            'my-habit-retrieve-update-destroy', args=[self.habit1.pk]
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.filter(pk=self.habit1.pk).count(), 0)

    def test_delete_foreign_habit_forbidden(self):
        """Тест: пользователь не может удалять чужую привычку."""
        url = reverse(
            'my-habit-retrieve-update-destroy', args=[self.habit2.pk]
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Habit.objects.filter(pk=self.habit2.pk).exists())

    def test_list_public_habits(self):
        """Тест просмотра списка публичных привычек."""
        # Создаем еще одну публичную привычку для user2
        Habit.objects.create(
            user=self.user2,
            place='В офисе',
            time=datetime.time(11, 0),
            action='Медитировать',
            estimated_time=300,
            is_public=True
        )
        url = reverse('public-habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # В списке должно быть 2 публичные привычки
        self.assertEqual(len(response.data['results']), 2)
        actions = {item['action'] for item in response.data['results']}
        self.assertIn('Делать зарядку', actions)
        self.assertIn('Медитировать', actions)

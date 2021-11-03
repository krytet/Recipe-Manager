from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import Client


User = get_user_model()


class UsersTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1_data = {
            'email' : 'Test111@TestsEmail.com',
            'username' : 'TestUser1',
            'first_name' : 'Test111',
            'last_name' : 'Test1111',
            'password' : 'TUserPass111'
        }
        response = self.client.post('/api/v1/users/', self.user1_data)
        self.assertEqual(response.status_code, 201, msg='Создание пользователя не удалось')

        # Получение токена 
        self.token1 = self.client.post('/api/v1/auth/token/login/', self.user1_data).data['auth_token']
        self.header1 = {
            'HTTP_AUTHORIZATION': f'Token {self.token1}',
        }
        response = self.client.get('/api/v1/users/', **self.header1)
        # TODO сделать проверку на количество

        self.assertEqual(response.status_code, 200, msg='Токен работает не коректно')
        # TODO подправить для анонимного пользователя
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200, msg='У анонимного пользователя должен быть доступ к списку пользователей')


        # Созание вторго пользователя
        self.user2_data = {
            'email' : 'Test222@TestsEmail.com',
            'username' : 'TestUser2',
            'first_name' : 'Test222',
            'last_name' : 'Test2222',
            'password' : 'TUserPass222'
        }
        response = self.client.post('/api/v1/users/', self.user2_data)
        self.assertEqual(response.status_code, 201, msg='Создание пользователя 2 не удалось')

        self.token2 = self.client.post('/api/v1/auth/token/login/', self.user2_data).data['auth_token']
        self.header2 = {
            'HTTP_AUTHORIZATION': f'Token {self.token2}',
        }
        




    #def tearDown(self):
    #    user = User.objects.get(email=self.user1_data['email'])
    #    print(User.objects.get(email=self.user1_data['email']))
    #    user.delete()
    #    user = User.objects.get(email=self.user2_data['email'])
    #    print(User.objects.get(email=self.user2_data['email']))
    #    user.delete()

    # Вывод списка пользователей
    def test_users_list(self):
        response = self.client.get('/api/v1/users/', **self.header1)
        self.assertEqual(response.status_code, 200, msg='У Пользователя1 нет доступа к списку пользователей')
        response = self.client.get('/api/v1/users/', **self.header2)
        self.assertEqual(response.status_code, 200, msg='У Пользователя2 нет доступа к списку пользователей')
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200, msg='У Анонимуса нет доступа к списку пользователей')
        # TODO провурку количества сделать


        
    
    # Вывод информации о пользователе
    def test_me_profile(self):
        response = self.client.get('/api/v1/users/me/')
        self.assertEqual(response.status_code, 401, msg='У Анономуса не должно быть доступа на просмотр своего профеля')

        ID = User.objects.get(email=self.user1_data['email']).id
        response = self.client.get(f'/api/v1/users/{ID}/')
        self.assertEqual(response.status_code, 401, msg='У Анономуса не должно быть доступа на просмотр профелей')

        response = self.client.get('/api/v1/users/me/', **self.header1)
        self.assertEqual(response.status_code, 200, 'У пользователя должна быть возможность просматривать свой профиль')

        response = self.client.get('/api/v1/users/me/', **self.header2)
        self.assertEqual(response.status_code, 200, 'У пользователя должна быть возможность просматривать свой профиль')

        response = self.client.get(f'/api/v1/users/{ID}/', **self.header2)
        self.assertEqual(response.status_code, 200, msg='У пользователя должна быть возможность просматривать профили')
        
    # Смена пароля
    def test_password(self):
        password = {
            'current_password' : self.user1_data['password'],
            'new_password' : f"{self.user1_data['password']}11",
        }
        response = self.client.post('/api/v1/users/set_password/',password, **self.header1)
        self.assertEqual(response.status_code, 201, msg='Пороль не помянялся, хотя должен был')
        response = self.client.post('/api/v1/users/set_password/',password)
        self.assertEqual(response.status_code, 401, msg='У Анонимунса не должно быть прав к изменению пароля')
        response = self.client.post('/api/v1/users/set_password/',password, **self.header2)
        self.assertEqual(response.status_code, 400, msg='Пароль не должен поменяться так как предыдущий введене не верно')
        password = {
            'current_password' : self.user2_data['password'],
            'new_password' : f"{self.user2_data['password']}22",
        }
        response = self.client.post('/api/v1/users/set_password/',password, **self.header2)
        self.assertEqual(response.status_code, 201, msg='Пороль не помянялся, хотя должен был')
        response = self.client.post('/api/v1/users/set_password/',password, **self.header2)
        self.assertEqual(response.status_code, 400, msg='Пароль не должен поменяться так как предыдущий введене не верно, так как поменяли его')

        
    # Подписки
    def test_subscription(self):
        # Подписаться на пользователя
        ID1 = User.objects.get(email=self.user1_data['email']).id
        ID2 = User.objects.get(email=self.user2_data['email']).id
        response = self.client.get(f'/api/v1/users/{ID2}/subscribe/', **self.header1)
        self.assertEqual(response.status_code, 200, msg='Подписка дожны быть удачной')
        response = self.client.get(f'/api/v1/users/{ID2}/subscribe/', **self.header1)
        self.assertEqual(response.data['errors'], 'Вы уже подписаны на данного пользователя')
        response = self.client.get(f'/api/v1/users/{ID1}/subscribe/', **self.header1)
        self.assertEqual(response.status_code, 400, msg='Дожна выйти ошибка, так как нельзя подписаться на себя')
        self.assertEqual(response.data['errors'], 'Вы не можете подписаться на самого себя', msg='Должны быть ошибка о невозможности подписаться на себя')
        # Вывести список подписок
        # TODO
        response = self.client.get('/api/v1/users/subscribe/', **self.header1)
        # Отписаться от пользователя
        response = self.client.delete(f'/api/v1/users/{ID2}/subscribe/', **self.header1)
        self.assertEqual(response.status_code, 204, msg='Отписка дожны быть удачной')

        # Вывести список подписок
        # TODO
        response = self.client.get('/api/v1/users/subscribe/', **self.header1)

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
        print(self.client.post('/api/v1/users/', self.user1_data))

        self.user2_data = {
            'email' : 'Test222@TestsEmail.com',
            'username' : 'TestUser2',
            'first_name' : 'Test222',
            'last_name' : 'Test2222',
            'password' : 'TUserPass222'
        }
        print(self.client.post('/api/v1/users/', self.user2_data))

        self.token1 = self.client.post('/api/v1/auth/token/login/', self.user1_data).data['auth_token']
        print(self.token1)
        self.token2 = self.client.post('/api/v1/auth/token/login/', self.user2_data).data['auth_token']
        print(self.token2)

    #def tearDown(self):
    #    user = User.objects.get(email=self.user1_data['email'])
    #    print(User.objects.get(email=self.user1_data['email']))
    #    user.delete()
    #    user = User.objects.get(email=self.user2_data['email'])
    #    print(User.objects.get(email=self.user2_data['email']))
    #    user.delete()

    # Вывод списка пользователей
    def test_users_list(self):
        print(self.client.get('/api/v1/users/'),)
        print(self.client.get('/api/v1/users/').__dict__)
        pass
    
    # Вывод информации о пользователе
    def test_me_profile(self):
        print(self.client.get('/api/v1/users/me/'))
        ID = User.objects.get(email=self.user1_data['email']).id
        print(self.client.get(f'/api/v1/users/{ID}/'))
        
    # Смена пароля
    def test_(self):
        pass
        
    # Подписки
    def test_(self):
        # Подписаться на пользователя
        # Вывести список подписок
        # Отписаться от пользователя
        # Вывести список подписок
        #
        #
        pass

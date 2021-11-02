from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import Client


User = get_user_model()

class RecipeTest(TestCase):

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
        print('!!!!!!!!!!!!!!!!!!!!!!TOKEN')
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

    
        
    # Рецепты
    def test_(self):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # Вывести список рецептов
        # Создать рецепт 1 пользователь 1
        # Создать рецепт 2 пользователь 1
        # Создать рецепт 1 пользователь 2
        # Создать рецепт 2 пользователь 2
        # Проверить список рецептов
        # Изменение рецепта
        #
        #
        pass
        
    # Теги
    def test_(self):
        # Посмотреть список тегов
        # Постотреть определенный тег
        
        pass
        
    # Ингридиенты
    def test_(self):
        # Посмотреть список ингридиентов
        # Посмотреть определеный ингридиент
        pass
        
    # Избранные 
    def test_(self):
        # Вывести список изброного
        # Вывести список рецептов и проверить отсуствие избранного в Р3 
        # Добавить рецепт П1 Р3 в избраное
        # Вывести список изброного
        #  Вывести список рецептов и проверить наличие изброного в Р3
        # Удалить изброное Р3
        # Вывести спиок рецептов и проверить наличие изброного
        # Вывести список изброного
        pass
        
    # Список поккупок
    def test_(self):
        # Вывести список покупок 
        # Проверить Р3 на отсутствие в корзине
        # Добавить Р3 в список покупок
        # Проверить Р3 на присудствие в списке покуупок
        # Вывести список покупок
        # Удалить из списка покупок Р3
        # Проверить Р3 на отсутсвие нахождения в карзине
        # Вывести список покупок
        pass
    
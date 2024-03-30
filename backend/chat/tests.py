import json

from django.test import TestCase

from chat.models import ChatRoom
from users.models import CustomUser


class ChatUsersViewTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            id=1,
            username='test1',
            password='test1',
            address='test1',
            postal_code=1234,
            city='test1',
            email_verified=True
        )
        self.user2 = CustomUser.objects.create_user(
            id=2,
            username='test2',
            password='test2',
            address='test2',
            postal_code=12345,
            city='test2',
            email_verified=True
        )
        self.user3 = CustomUser.objects.create_user(
            id=3,
            username='test3',
            password='test3',
            address='test3',
            postal_code=12345,
            city='test2',
        )
        self.chatroom = ChatRoom.objects.create(title='Test Chat Room')
        self.chatroom.members.add(self.user1, self.user2)

    def test_chat_users_success(self):
        token = self.get_user_token(self.user1.username, 'test1')
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/chat/chat-users/', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue('users' in data)
        users = data['users']
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['id'], self.user2.id)

    def test_chat_users_fail_invalid_token(self):
        headers = {'Authorization': 'Bearer invalidtoken'}
        response = self.client.get('/chat/chat-users/', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_chat_users_fail_unauthorized(self):
        token = self.get_user_token(self.user3.username, 'test3')
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/chat/chat-users/', headers=headers)
        self.assertEqual(response.status_code, 401)

    def get_user_token(self, username, password):
        response_login = self.client.post('/users/login/', {'username': username, 'password': password},
                                          format='json')
        print(response_login.data)
        return response_login.data.get('token', '')


# Create your tests here.
class ChatViewTest(TestCase):

    def setUp(self):
        CustomUser.objects.create_user(
            id=1,
            username='test',
            password='test',
            address='test',
            postal_code=1234,
            city='test',
            email_verified=True
        )
        CustomUser.objects.create_user(
            id=2,
            username='test2',
            password='test2',
            address='test2',
            postal_code=12345,
            city='test2',
            email_verified=True
        )
        CustomUser.objects.create_user(
            id=3,
            username='test3',
            password='test3',
            address='test3',
            postal_code=12345,
            city='test3',
            email_verified=True
        )
        chat = ChatRoom.objects.create(
            id=1,
            title='test',

        )
        chat.members.add(3, 2)

    def tearDown(self):
        super().tearDown()

    def test_get_chatroom_not_exists(self):
        data_chat = {"currentUserID": 1, "otherUserID": 2}
        response = self.client.post('/chat/chatroom/', data_chat, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_chatroom_fail(self):
        data_chat = {"currentUserID": 5, "otherUserID": 2}
        response = self.client.post('/chat/chatroom/', data_chat, format='json')
        self.assertEqual(response.status_code, 404)

    def test_get_chatroom_exists(self):
        data_chat = {"currentUserID": 3, "otherUserID": 2}
        response = self.client.post('/chat/chatroom/', data_chat, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_chatroom_succes(self):
        data = {'username': 'test2', 'password': 'test2'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token']
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/chat/chatroom/1', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_chatroom_fail_invalid_token(self):
        data = {'username': 'test', 'password': 'test'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token'] + 'invalid'
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/chat/chatroom/1', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_get_chatroom_fail_user_not_member(self):
        data = {'username': 'test', 'password': 'test'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token']
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/chat/chatroom/1', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_get_messages_succes(self):
        data = {'username': 'test2', 'password': 'test2'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token']
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/chat/1/messages/', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_messages_fail_invalid_token(self):
        data = {'username': 'test', 'password': 'test'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token'] + 'invalid'
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/chat/1/messages/', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_get_messages_fail_user_not_member(self):
        data = {'username': 'test', 'password': 'test'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token']
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/chat/1/messages/', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_post_message_fail_method(self):
        data = {'username': 'test2', 'password': 'test2'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token']
        headers = {'Authorization': 'Bearer ' + token}
        data_message = {"content": "This is the message content.", "username": "sender_username"}
        response = self.client.get('/chat/1/post_message/', data=data_message, headers=headers, format='json')
        self.assertEqual(response.status_code, 405)

    def test_post_message_succes(self):
        data = {'username': 'test2', 'password': 'test2'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token']
        headers = {'Authorization': 'Bearer ' + token}
        data_message = {"content": "This is the message content.", "username": "sender_username"}
        data_message_json = json.dumps(data_message)  # Convert to JSON string
        data_message_bytes = data_message_json.encode('utf-8')  # Convert to bytes
        response = self.client.post('/chat/1/post_message/', data_message_bytes, headers=headers,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_message_fail_invalid_token(self):
        data = {'username': 'test', 'password': 'test'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token'] + 'invalid'
        headers = {'Authorization': 'Bearer ' + token}
        data_message = {"content": "This is the message content.", "username": "sender_username"}
        data_message_json = json.dumps(data_message)  # Convert to JSON string
        data_message_bytes = data_message_json.encode('utf-8')
        response = self.client.post('/chat/1/post_message/', data_message_bytes, headers=headers,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_post_message_fail_user_not_member(self):
        data = {'username': 'test', 'password': 'test'}
        response_login = self.client.post('/users/login/', data, format='json')
        token = response_login.data['token']
        headers = {'Authorization': 'Bearer ' + token}
        data_message = {"content": "This is the message content.", "username": "sender_username"}
        data_message_json = json.dumps(data_message)
        data_message_bytes = data_message_json.encode('utf-8')
        response = self.client.post('/chat/1/post_message/', data_message_bytes, headers=headers,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

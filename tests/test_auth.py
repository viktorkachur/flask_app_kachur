import unittest
from app import create_app, db
from app.models import User
from sqlalchemy import select


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):

        response = self.client.post('/users/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        user = db.session.scalar(select(User).where(User.username == 'newuser'))
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@example.com')
        self.assertIn(
            b'\xd0\x90\xd0\xba\xd0\xb0\xd1\x83\xd0\xbd\xd1\x82 \xd1\x81\xd1\x82\xd0\xb2\xd0\xbe\xd1\x80\xd0\xb5\xd0\xbd\xd0\xbe',
            response.data)

    def test_login_and_logout(self):

        user = User(username='loginuser', email='login@example.com', password='password123')
        db.session.add(user)
        db.session.commit()


        response = self.client.post('/users/login', data={
            'email': 'login@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
        self.assertIn(b'loginuser', response.data)


        response = self.client.get('/users/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b'\xd0\x92\xd0\xb8 \xd0\xb2\xd0\xb8\xd0\xb9\xd1\x88\xd0\xbb\xd0\xb8 \xd0\xb7 \xd1\x81\xd0\xb8\xd1\x81\xd1\x82\xd0\xb5\xd0\xbc\xd0\xb8',
            response.data)
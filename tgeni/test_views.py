import app
import app.models       as models
import os
import unittest

from app                import tgeni, db
from flask              import url_for
from flask_login        import current_user
from flask_testing      import TestCase

class BaseTestCase(TestCase):
    def create_app(self):
        tgeni.config.from_object('config.TestConfig')
        return tgeni
    def setUp(self):
        db.create_all()
    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserTestCase(BaseTestCase):
    #####################
    ## User test cases ##
    #####################

    def test_register(self):
        response = self.client.post('/register',
                        data=dict(username='newuser', email='test@email.web',
                        password="it's a secret to everyone"),
                    follow_redirects=True)
        # test lookup
        found_user = app.models.User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(found_user)
        # test fields
        self.assertEqual(found_user.username, 'newuser')
        self.assertEqual(found_user.email, 'test@email.web')
        self.assertTrue(found_user.password_matches("it's a secret to everyone"))

    def test_register_invalid(self):
        pass # --! TODO

    def test_signin(self):
        user = models.User( username='testuser',
                            email   ='test@email.web',
                            password="testpwd")
        db.session.add(user)
        db.session.commit()
        with self.client:
            # test redirect
            response = self.client.post(url_for('signin'),
                            data=dict(username='testuser', password="testpwd"))
            self.assert_redirects(response, url_for('index'))
            # test user
            self.assertTrue(current_user.username == 'testuser')
            self.assertFalse(current_user.is_anonymous)


    def test_signin_invalid_username(self):
        with self.client:
            # test redirect
            response = self.client.post(url_for('signin'),
                            data=dict(username='invalid', password='invalid'),
                            follow_redirects=True)
            self.assertTrue('Invalid username or password' in str(response.data))

    def test_signin_invalid_password(self):
        user = models.User( username='testuser',
                            email   ='test@email.web',
                            password="testpwd")
        db.session.add(user)
        db.session.commit()
        with self.client:
            # test redirect
            response = self.client.post(url_for('signin'),
                            data=dict(username='testuser', password='invalid'),
                            follow_redirects=True)
            self.assertTrue('Invalid username or password' in str(response.data))

    def test_signout(self):
        user = models.User( username='testuser',
                            email   ='test@email.web',
                            password="testpwd")
        db.session.add(user)
        db.session.commit()
        with self.client:
            self.client.post(url_for('signin'),
                        data=dict(username='testuser', password="testpwd"))
            self.client.get(url_for('signout'))
            self.assertTrue(current_user.is_anonymous)



class HomeTestCase(BaseTestCase):

    def test_home(self):
        with self.client:
            # 302 = redirect
            response = self.client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue('Travel Geni' in str(response.data))
            # 200 = OK
            response = self.client.get('/home')
            self.assertEqual(response.status_code, 200)
            self.assertTrue('Travel Geni' in str(response.data))



if __name__ == '__main__':
    unittest.main()

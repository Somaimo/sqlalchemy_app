from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, TeamModel, CityModel

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
'd4c74594d841139328695756648b6bd6'
'?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        c = CityModel(name='Liverpool')
        db.session.add(c)
        db.session.commit()
        city = CityModel.query.first()
        t = TeamModel(name='FC Liverpool', city_id=city.id, create_user_id=1)
        db.session.add(u1)
        db.session.add(t)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(t.followers.all(), [])

        u1.follow(t)
        db.session.commit()
        self.assertTrue(u1.is_following(t))
        self.assertEqual(u1.followed.count(), 1)
        self.assertTrue(t.followers.count(), 1)
        self.assertEqual(t.followers.first().username, 'john')

        u1.unfollow(t)
        db.session.commit()
        self.assertFalse(u1.is_following(t))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(t.followers.count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
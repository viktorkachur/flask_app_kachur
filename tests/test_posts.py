import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory
from app.models import User
import datetime


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()


        self.user = User(username='testauthor', email='author@example.com', password='password')
        db.session.add(self.user)
        db.session.commit()
        self.user_id = self.user.id  # Запам'ятовуємо ID


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_post(self):
        response = self.client.post("/post/add_post", data={
            "title": "Мій перший пост",
            "content": "Це тест TDD!",
            "is_active": True,
            "publish_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "category": PostCategory.tech.name,
            "author_id": self.user_id  # <-- Додаємо ID автора
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'\xd0\x9f\xd0\xbe\xd1\x81\xd1\x82', response.data)
        self.assertIn(
            b'\xd1\x83\xd1\x81\xd0\xbf\xd1\x96\xd1\x88\xd0\xbd\xd0\xbe \xd0\xb4\xd0\xbe\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xbe',
            response.data)

        post = db.session.scalars(
            db.select(Post).filter_by(title="Мій перший пост")
        ).first()

        self.assertIsNotNone(post)
        self.assertEqual(post.user_id, self.user_id)  # Перевіряємо автора


    def test_list_posts(self):
        post1 = Post(title="Тестовий Пост 1", content="Вміст 1", user_id=self.user_id)  # <-- +user_id
        db.session.add(post1)
        db.session.commit()

        response = self.client.get("/post/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'\xd0\xa2\xd0\xb5\xd1\x81\xd1\x82\xd0\xbe\xd0\xb2\xd0\xb8\xd0\xb9 \xd0\x9f\xd0\xbe\xd1\x81\xd1\x82 1',
            response.data)


    def test_view_post_detail(self):
        post1 = Post(title="Детальний Пост", content="Вміст детального поста", user_id=self.user_id)  # <-- +user_id
        db.session.add(post1)
        db.session.commit()

        response = self.client.get(f"/post/{post1.id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'\xd0\x94\xd0\xb5\xd1\x82\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb8\xd0\xb9 \xd0\x9f\xd0\xbe\xd1\x81\xd1\x82',
            response.data)


    def test_update_post(self):
        post_to_edit = Post(title="Старий Заголовок", content="Старий вміст", user_id=self.user_id)  # <-- +user_id
        db.session.add(post_to_edit)
        db.session.commit()

        new_data = {
            "title": "Оновлений Заголовок",
            "content": "Оновлений вміст",
            "is_active": True,
            "publish_date": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "category": PostCategory.news.name,
            "author_id": self.user_id
        }

        response = self.client.post(
            f"/post/{post_to_edit.id}/update",
            data=new_data,
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        updated_post = db.session.get(Post, post_to_edit.id)
        self.assertEqual(updated_post.title, "Оновлений Заголовок")


    def test_delete_post(self):
        post_to_delete = Post(title="Пост на видалення", content="Вміст", user_id=self.user_id)  # <-- +user_id
        db.session.add(post_to_delete)
        db.session.commit()

        post_id = post_to_delete.id

        response = self.client.post(
            f"/post/{post_id}/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)


    def test_404_not_found(self):
        response = self.client.get("/post/99999")
        self.assertEqual(response.status_code, 404)
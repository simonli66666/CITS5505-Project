import unittest
from app import create_app, db
from app.models import User, Post, Comments, Like
from app.setting import TestingConfig

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.testApp = create_app(TestingConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_test_data(self):
        User.query.filter_by(username='testuser').delete()
        db.session.commit()
        
        user = User(username='testuser', nickname='testnickname', password='testpassword')
        db.session.add(user)
        db.session.commit()
        
        post = Post(
            title='Test Post', 
            content='This is a test post content.', 
            author_id=user.id,
            ingredient1='Ingredient 1', 
            ingredient2='Ingredient 2', 
            ingredient3='Ingredient 3', 
            ingredient4='Ingredient 4',
            ingredient5='Ingredient 5', 
            ingredient6='Ingredient 6', 
            servings=1, 
            prep_time=10, 
            cooking_time=10,
            calories=100
        )
        db.session.add(post)
        db.session.commit()

    def test_user_registration(self):
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.nickname, 'testnickname')

    def test_add_post(self):
        user = User.query.filter_by(username='testuser').first()
        post = Post(
            title='Another Test Post', 
            content='This is another test post content.', 
            author_id=user.id,
            ingredient1='Ingredient 1', 
            ingredient2='Ingredient 2', 
            ingredient3='Ingredient 3', 
            ingredient4='Ingredient 4',
            ingredient5='Ingredient 5', 
            ingredient6='Ingredient 6', 
            servings=1, 
            prep_time=10, 
            cooking_time=10,
            calories=100
        )
        db.session.add(post)
        db.session.commit()
        
        saved_post = Post.query.filter_by(title='Another Test Post').first()
        self.assertIsNotNone(saved_post)
        self.assertEqual(saved_post.content, 'This is another test post content.')

    def test_add_comment(self):
        user = User.query.filter_by(username='testuser').first()
        post = Post.query.first()
        comment = Comments(body='This is a test comment', author_id=user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        
        saved_comment = Comments.query.filter_by(author_id=user.id).first()
        self.assertIsNotNone(saved_comment)
        self.assertEqual(saved_comment.body, 'This is a test comment')

    def test_user_badges(self):
        user = User.query.filter_by(username='testuser').first()
        post = Post.query.first()
        comment = Comments(body='This is another test comment', author_id=user.id, post_id=post.id)
        like = Like(user_id=user.id, post_id=post.id)
        
        db.session.add(comment)
        db.session.add(like)
        db.session.commit()
        
        expected_badges = 20 + user.post_num * 5 + user.like_num * 2 + user.comment_num * 2 + user.selfcomment_num * 2
        self.assertEqual(user.badges, expected_badges)

    def test_update_user_info(self):
        user = User.query.filter_by(username='testuser').first()
        user.email = 'testuser@example.com'
        user.mobile = '1234567890'
        db.session.commit()
        
        updated_user = User.query.filter_by(username='testuser').first()
        self.assertEqual(updated_user.email, 'testuser@example.com')
        self.assertEqual(updated_user.mobile, '1234567890')

    def test_add_multiple_comments(self):
        user = User.query.filter_by(username='testuser').first()
        post = Post.query.first()
        
        comment1 = Comments(body='First test comment', author_id=user.id, post_id=post.id)
        comment2 = Comments(body='Second test comment', author_id=user.id, post_id=post.id)
        db.session.add(comment1)
        db.session.add(comment2)
        db.session.commit()
        
        comments = Comments.query.filter_by(author_id=user.id).all()
        self.assertEqual(len(comments), 2)
        self.assertIn('First test comment', [comment.body for comment in comments])
        self.assertIn('Second test comment', [comment.body for comment in comments])

if __name__ == '__main__':
    unittest.main()

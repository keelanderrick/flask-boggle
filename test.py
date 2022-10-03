from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.text_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('plays'))
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Current Score:', response.data)
            self.assertIn(b'Time Remaining:', response.data)

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['T', 'H', 'E', 'S', 'E'], ['T', 'H', 'E', 'S', 'E'], [
                    'T', 'H', 'E', 'S', 'E'], ['T', 'H', 'E', 'S', 'E'], ['T', 'H', 'E', 'S', 'E']]
        response = self.client.get('/check-word?word=these')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['T', 'H', 'E', 'S', 'E'], ['T', 'H', 'E', 'S', 'E'], [
                    'T', 'H', 'E', 'S', 'E'], ['T', 'H', 'E', 'S', 'E'], ['T', 'H', 'E', 'S', 'E']]
        response = self.client.get('/check-word?word=those')
        self.assertEqual(response.json['result'], 'ok')

    def test_non_word(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=sdafsnfenn')
        self.assertEqual(response.json['result'], 'not-word')

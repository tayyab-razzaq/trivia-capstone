"""Module for tests."""

import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import app
from flaskr.constants import (
    ERROR_MESSAGES, MISSING_AUTHORIZATION, MISSING_BEARER,
    MISSING_BEARER_TOKEN, MISSING_TOKEN, STATUS_BAD_REQUEST,
    STATUS_CREATED, STATUS_METHOD_NOT_ALLOWED, STATUS_NOT_FOUND,
    STATUS_NO_CONTENT, STATUS_OK, STATUS_UNAUTHORIZED
)

from models import get_database_path, setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case."""

    def setUp(self):
        """
        Define test variables and initialize app.

        :return:
        """
        self.app = app
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = get_database_path(self.database_name)
        setup_db(self.app, self.database_path)

        self.question = {
            "question": "Test 1",
            "answer": "Answer 1",
            "category": 1,
            "difficulty": 1
        }

        self.updated_question = {
            "question": "Test 2",
            "answer": "Answer 2",
            "category": 2,
            "difficulty": 2
        }

        with open('./tokens.json') as json_file:
            data = json.load(json_file)
            self.member_headers = {
                'Authorization': 'Bearer {}'.format(data.get('member'))
            }
            self.manager_headers = {
                'Authorization': 'Bearer {}'.format(data.get('manager'))
            }

        self.no_bearer_token = {
            'Authorization': '{}'.format(data.get('member'))
        }

        self.wrong_bearer_token = {
            'Authorization': 'Bearer {} fail'.format(data.get('member'))
        }

        self.no_token = {
            'Authorization': 'Bearer'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_categories_success(self):
        """
        Success test case for get categories route.

        :return:
        """
        response = self.client().get('/categories')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('categories')))

    def test_get_categories_failed(self):
        """
        Fail test case for get categories route.

        :return:
        """
        response = self.client().post('/categories')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_get_questions_success(self):
        """
        Success case for get questions.

        :return:
        """
        response = self.client().get('/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('categories')))
        self.assertTrue(len(json_data.get('questions')))
        self.assertTrue(json_data.get('total_questions'))

    def test_get_questions_failed(self):
        """
        Fail case for get questions.

        :return:
        """
        response = self.client().get('/questions?page=-1000')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_NOT_FOUND]
        )

    def test_search_questions_success(self):
        """
        Success case of search questions api.

        :return:
        """
        data = {
            "searchTerm": "The"
        }
        response = self.client().post('/questions/filter', json=data)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('questions')))
        self.assertTrue(json_data.get('total_questions'))

    def test_search_questions_failed(self):
        """
        Success case of search questions api with method not allowed error.

        :return:
        """
        response = self.client().get('/questions/filter', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_get_questions_by_category_success(self):
        """
        Success case for get questions by category.

        :return:
        """
        response = self.client().get('/categories/1/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('questions')))
        self.assertTrue(json_data.get('total_questions'))
        self.assertTrue(len(json_data.get('current_category')))

    def test_get_questions_by_category_failed_method_not_allowed(self):
        """
        Fail case for get questions by category with method not allowed error.

        :return:
        """
        response = self.client().post('/categories/1/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_get_questions_by_category_not_found(self):
        """
        Fail case for get questions by category with method not found.

        :return:
        """
        response = self.client().get('/categories/1000/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_NOT_FOUND]
        )

    def test_add_question_success(self):
        """
        Success case of add question test case.

        :return:
        """
        response = self.client().post(
            '/questions', json=self.question, headers=self.manager_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_CREATED)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(json_data.get('id'))

    def test_add_question_failed_method_not_allowed(self):
        """
        Fail case of add question test case with method not allowed error.

        :return:
        """
        response = self.client().put('/questions', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_add_question_failed_bad_request(self):
        """
        Fail case of add question test case with bad request error.

        :return:
        """
        response = self.client().post(
            '/questions', json={}, headers=self.manager_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_BAD_REQUEST]
        )

    def test_add_question_failed_no_auth(self):
        """
        Fail case of add question test case without authorization.

        :return:
        """
        response = self.client().post('/questions', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_AUTHORIZATION)

    def test_add_question_failed_no_bearer_token(self):
        """
        Fail case of add question test case with no bearer token.

        :return:
        """
        response = self.client().post(
            '/questions', json={}, headers=self.no_bearer_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_BEARER)

    def test_add_question_failed_wrong_bearer_token(self):
        """
        Fail case of add question test case with wrong bearer token.

        :return:
        """
        response = self.client().post(
            '/questions', json={}, headers=self.wrong_bearer_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_BEARER_TOKEN)

    def test_add_question_failed_no_token(self):
        """
        Fail case of add question test case with no token in auth.

        :return:
        """
        response = self.client().post(
            '/questions', json={}, headers=self.no_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_TOKEN)

    def test_add_question_failed_unauthorized(self):
        """
        Fail case of add question test case without permission on that api.

        :return:
        """
        response = self.client().post(
            '/questions', json={}, headers=self.member_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_UNAUTHORIZED]
        )

    def test_update_question_success(self):
        """
        Success case of update question test case.

        :return:
        """
        response = self.client().post(
            '/questions', json=self.question, headers=self.manager_headers)
        question_id = response.get_json().get('id')
        response = self.client().patch(
            f'/questions/{question_id}',
            json=self.updated_question, headers=self.manager_headers)
        json_data = response.get_json()
        updated_questions = {**self.updated_question, "id": question_id}
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('question'), updated_questions)

    def test_update_question_failed_method_not_allowed(self):
        """
        Fail case of update question test case with method not allowed error.

        :return:
        """
        response = self.client().post(
            '/questions', json=self.question, headers=self.manager_headers)
        question_id = response.get_json().get('id')
        response = self.client().put(f'/questions/{question_id}', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_update_question_failed_no_auth(self):
        """
        Fail case of update question test case without authorization.

        :return:
        """
        response = self.client().patch('/questions/1', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_AUTHORIZATION)

    def test_update_question_failed_no_bearer_token(self):
        """
        Fail case of update question test case with no bearer token.

        :return:
        """
        response = self.client().patch(
            '/questions/1', json={}, headers=self.no_bearer_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_BEARER)

    def test_update_question_failed_wrong_bearer_token(self):
        """
        Fail case of update question test case with wrong bearer token.

        :return:
        """
        response = self.client().patch(
            '/questions/1', json={}, headers=self.wrong_bearer_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_BEARER_TOKEN)

    def test_update_question_failed_no_token(self):
        """
        Fail case of update question test case with no token in auth.

        :return:
        """
        response = self.client().patch(
            '/questions/1', json={}, headers=self.no_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_TOKEN)

    def test_update_question_failed_unauthorized(self):
        """
        Fail case of update question test case without permission on that api.

        :return:
        """
        response = self.client().patch(
            '/questions/1', json={}, headers=self.member_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_UNAUTHORIZED]
        )

    def test_delete_question_success(self):
        """
        Success case of delete question test case.

        :return:
        """
        save_response = self.client().post(
            '/questions', json=self.question, headers=self.manager_headers)
        question_id = save_response.get_json().get('id')
        response = self.client().delete(
            f'/questions/{question_id}', headers=self.manager_headers)
        self.assertEqual(response.status_code, STATUS_NO_CONTENT)

    def test_delete_question_failed_method_not_allowed(self):
        """
        Fail case of delete question test case with method not allowed error.

        :return:
        """
        response = self.client().put('/questions/1')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_delete_question_failed_not_found(self):
        """
        Not found failed case of delete question test case.

        :return:
        """
        response = self.client().delete(
            '/questions/-1000', headers=self.manager_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_NOT_FOUND]
        )

    def test_delete_question_failed_no_auth(self):
        """
        Fail case of delete question test case without authorization.

        :return:
        """
        response = self.client().delete('/questions/1')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_AUTHORIZATION)

    def test_delete_question_failed_no_bearer_token(self):
        """
        Fail case of delete question test case with no bearer token.

        :return:
        """
        response = self.client().delete(
            '/questions/1', headers=self.no_bearer_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_BEARER)

    def test_delete_question_failed_wrong_bearer_token(self):
        """
        Fail case of delete question test case with wrong bearer token.

        :return:
        """
        response = self.client().delete(
            '/questions/1', headers=self.wrong_bearer_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_BEARER_TOKEN)

    def test_delete_question_failed_no_token(self):
        """
        Fail case of delete question test case with no token in auth.

        :return:
        """
        response = self.client().delete('/questions/1', headers=self.no_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_TOKEN)

    def test_delete_question_failed_unauthorized(self):
        """
        Fail case of delete question test case without permission on that api.

        :return:
        """
        response = self.client().delete(
            '/questions/1', headers=self.member_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_UNAUTHORIZED]
        )

    def test_play_quiz_success_member_role(self):
        """
        Success case for play quiz api with member.

        :return:
        """
        data = {
            "quiz_category": {
                "id": 1
            },
            "previous_questions": []
        }
        response = self.client().post(
            '/quizzes', json=data, headers=self.member_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('question')))

    def test_play_quiz_success_manager_role(self):
        """
        Success case for play quiz api with manager role.

        :return:
        """
        data = {
            "quiz_category": {
                "id": 1
            },
            "previous_questions": []
        }
        response = self.client().post(
            '/quizzes', json=data, headers=self.manager_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('question')))

    def test_play_quiz_failed_method_not_allowed(self):
        """
        Fail case for play quiz api with method not allowed error.

        :return:
        """
        response = self.client().get('/quizzes', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_play_quiz_failed_bad_request(self):
        """
        Fail case for play quiz api with method bad request.

        :return:
        """
        response = self.client().post(
            '/quizzes', json={}, headers=self.member_headers)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_BAD_REQUEST]
        )

    def test_play_quiz_failed_no_auth(self):
        """
        Fail case of play quiz api test case without authorization.

        :return:
        """
        response = self.client().post('/quizzes', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_AUTHORIZATION)

    def test_play_quiz_failed_no_bearer_token(self):
        """
        Fail case of play quiz api test case with no bearer token.

        :return:
        """
        response = self.client().post(
            '/quizzes', json={}, headers=self.no_bearer_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_BEARER)

    def test_play_quiz_failed_wrong_bearer_token(self):
        """
        Fail case of play quiz api test case with wrong bearer token.

        :return:
        """
        response = self.client().post(
            '/quizzes', json={}, headers=self.wrong_bearer_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_BEARER_TOKEN)

    def test_play_quiz_failed_no_token(self):
        """
        Fail case of play quiz api test case with no token in auth.

        :return:
        """
        response = self.client().post(
            '/quizzes', json={}, headers=self.no_token)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_UNAUTHORIZED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), MISSING_TOKEN)

    def tearDown(self):
        """
        Execute after reach test.

        :return:
        """
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

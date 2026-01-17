import pytest
from django.urls import reverse

from quiz.models import Category, Question, Quiz


@pytest.mark.django_db
class TestCategoryAPI:
    def test_create_and_list_categories(self, client):
        url = reverse('create-and-list-category')
        category_title = 'Math'
        response = client.post(
            url, {'title': category_title}, content_type='application/json'
        )
        assert response.status_code == 201

        response = client.get(url)
        assert response.status_code == 200
        assert response.json()[0]['title'] == category_title

    def test_update_and_delete_category(self, client):
        updated_category = 'Second'
        category = Category.objects.create(title='First')
        url = reverse('detail-get-update-delete-category', args=[category.id])

        response = client.put(
            url, {'title': updated_category}, content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json()['title'] == updated_category

        response = client.delete(url)
        assert response.status_code == 200
        assert Category.objects.count() == 0


@pytest.mark.django_db
class TestQuizAPI:
    def test_create_and_list_quizzes(self, client):
        title = 'Python'
        description = 'PythonDesc'
        url = reverse('create-and-list-quiz')
        response = client.post(
            url,
            {'title': title, 'description': description},
            content_type='application/json',
        )
        assert response.status_code == 201

        response = client.get(url)
        assert response.status_code == 200
        assert response.json()[0]['title'] == title
        assert response.json()[0]['description'] == description

    def test_update_and_delete_quiz(self, client):
        updated_title = 'SecondTitle'
        updated_description = 'SecondDesc'
        quiz = Quiz.objects.create(title='FirstTitle', description='FirstDesc')
        url = reverse('detail-get-update-delete-quiz', args=[quiz.id])

        response = client.put(
            url,
            {
                'title': updated_title,
                'description': updated_description
            },
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json()['title'] == updated_title
        assert response.json()['description'] == updated_description

        response = client.delete(url)
        assert response.status_code == 200
        assert Quiz.objects.count() == 0

    def test_random_question(self, client):
        category = Category.objects.create(title='IT')
        quiz = Quiz.objects.create(title='Python', description='shhhh')
        text = '2+2?'
        Question.objects.create(
            quiz=quiz,
            category=category,
            text=text,
            options=['3', '4'],
            correct_answer=1,
            difficulty='easy',
        )
        url = reverse('quiz-random-question', args=[quiz.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()['text'] == text

    def test_by_title(self, client):
        Quiz.objects.create(title='Test 1', description='1')
        Quiz.objects.create(title='Test 2', description='2')
        Quiz.objects.create(title='Base', description='WOW')
        url = reverse('get-by-title-quiz', kwargs={'title': 'Test'})
        response = client.get(url)
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 2
        assert all('Test' in q['title'] for q in results)


@pytest.mark.django_db
class TestQuestionAPI:
    def setup_method(self):
        self.category = Category.objects.create(title='Chemistry')
        self.quiz = Quiz.objects.create(
            title='Periodic table',
            description='Some chemical joke'
        )

    def test_create_and_list_questions(self, client):
        url = reverse('create-and-list-question')
        text = '2+2?'
        response = client.post(
            url,
            {
                'quiz': self.quiz.id,
                'category': self.category.id,
                'text': '2+2?',
                'options': ['3', '4'],
                'correct_answer': 1,
                'difficulty': 'easy',
            },
            content_type='application/json',
        )
        assert response.status_code == 201

        response = client.get(url)
        assert response.status_code == 200
        assert response.json()[0]['text'] == text

    def test_update_and_delete_question(self, client):
        updated_text = '2+2?'
        updated_options = ['1', '3', '4']

        question = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            text='1+1?',
            options=['1', '2'],
            correct_answer=1,
            difficulty='easy',
        )
        url = reverse('detail-get-update-delete-question', args=[question.id])

        response = client.put(
            url,
            {
                'quiz': self.quiz.pk,
                'category': self.category.pk,
                'text': updated_text,
                'options': updated_options,
                'correct_answer': 2,
                'difficulty': question.difficulty
            },
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json()['text'] == updated_text
        assert response.json()['options'] == updated_options

        response = client.delete(url)
        assert response.status_code == 200
        assert Question.objects.count() == 0

    def test_by_text(self, client):
        Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            text='5+5?',
            options=['6', '10'],
            correct_answer=0,
            difficulty='easy',
        )
        Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            text='7+7?',
            options=['10', '14'],
            correct_answer=0,
            difficulty='easy',
        )
        url = reverse('get-by-text-question', kwargs={'text': '5+5'})
        response = client.get(url)
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]['text'] == '5+5?'

    def test_check_answer(self, client):
        question = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            text='2+7?',
            options=['3', '4', '9'],
            correct_answer=2,
            difficulty='easy',
        )
        url = reverse('check-answer', args=[question.id])
        response = client.post(
            url,
            {'user_answer': '9'},
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json()['answer_correct'] is True

        response = client.post(
            url,
            {'user_answer': '4'},
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json()['answer_correct'] is False

        response = client.post(
            url,
            {'user_answer': '3'},
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json()['answer_correct'] is False

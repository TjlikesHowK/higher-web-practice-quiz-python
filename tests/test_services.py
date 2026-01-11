import pytest

from quiz.models import Category, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


@pytest.mark.django_db
class TestCategoryService:
    def setup_method(self):
        self.service = CategoryService()

    def test_create_and_get_category(self):
        category_title = 'Chemistry'
        category = self.service.create_category(category_title)
        fetched = self.service.get_category(category.id)
        assert fetched.title == category_title

    def test_update_category(self):
        updated_category = 'Second'
        category = Category.objects.create(title='Fisrt')
        updated = self.service.update_category(
            category.id,
            {'name': updated_category}
        )
        assert updated.name == updated_category

    def test_delete_category(self):
        category = Category.objects.create(title='Temp')
        self.service.delete_category(category.id)
        assert Category.objects.count() == 0


@pytest.mark.django_db
class TestQuizService:
    def setup_method(self):
        self.service = QuizService()

    def test_create_and_get_quiz(self):
        title = 'Title1'
        quiz = self.service.create_quiz(
            {
                'title': title,
                'description': 'Some description'
            }
        )
        fetched = self.service.get_quiz(quiz.id)
        assert fetched.title == title

    def test_update_quiz(self):
        updated_quiz = 'SecondQuiz'
        quiz = Quiz.objects.create(
            title='FirstQuiz',
            description='SameDescription'
        )
        updated = self.service.update_quiz(
            quiz.id,
            {'title': updated_quiz}
        )
        assert updated.title == updated_quiz
        assert updated.description == quiz.description

    def test_delete_quiz(self):
        quiz = Quiz.objects.create(title='Quiz', description='Desc')
        self.service.delete_quiz(quiz.id)
        assert Quiz.objects.count() == 0


@pytest.mark.django_db
class TestQuestionService:
    def setup_method(self):
        self.question_service = QuestionService()
        self.category = Category.objects.create(title='IT')
        self.quiz = Quiz.objects.create(title='Python', description='shhhh')

    def test_create_and_get_question(self):
        question = self.question_service.create_question(
            self.quiz.id,
            {
                'category': self.category,
                'description': 'desc',
                'text': '2+2?',
                'options': ['3', '4', '5'],
                'correct_answer': 1,
                'explanation': '+',
                'difficulty': 'easy',
            },
        )
        fetched = self.question_service.get_question(question.id)
        assert fetched.correct_answer == 1
        assert fetched.options[fetched.correct_answer] == '4'

    def test_update_question(self):
        updated_text = '2+5?'
        updated_options = ['4', '7']
        question = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            description='desc',
            text='2+3?',
            options=['4', '5'],
            correct_answer='5',
            explanation='',
            difficulty='easy',
        )
        updated = self.question_service.update_question(
            question.id,
            {
                'text': updated_text,
                'options': updated_options
            }
        )
        assert updated.text == updated_text
        assert updated.options == updated_options

    def test_delete_question(self):
        question = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            description='',
            text='2-1',
            options=['1', '2'],
            correct_answer=0,
            explanation='-',
            difficulty='easy',
        )
        self.question_service.delete_question(question.id)
        assert Question.objects.count() == 0

    def test_check_answer(self):
        question = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            description='',
            text='2+8?',
            options=['5', '10'],
            correct_answer=1,
            explanation='',
            difficulty='easy',
        )
        assert self.question_service.check_answer(question.id, '10') is True
        assert self.question_service.check_answer(question.id, '5') is False

    def test_get_question_by_text(self):
        question1 = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            description='Desc 1',
            text='2+2?',
            options=['1', '4', '8'],
            correct_answer=1,
            explanation='+',
            difficulty='easy',
        )
        question2 = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            description='Desc 2',
            text='2*2',
            options=['4', '6'],
            correct_answer=1,
            explanation='*',
            difficulty='easy',
        )

        results = self.question_service.get_questions_by_text('2+2')
        assert question1 in results
        assert question2 not in results

        results = self.question_service.get_questions_by_text('2*2')
        assert question2 in results
        assert question1 not in results

    def test_random_question_from_quiz(self):
        question1 = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            description='Desc 1',
            text='2+2?',
            options=['1', '4', '8'],
            correct_answer=1,
            explanation='+',
            difficulty='easy',
        )
        question2 = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            description='Desc 2',
            text='2*2',
            options=['4', '8'],
            correct_answer=0,
            explanation='*',
            difficulty='easy',
        )
        question = self.question_service.random_question_from_quiz(
            self.quiz.id
        )
        assert question in [question1, question2]
        assert question.quiz_id == self.quiz.id

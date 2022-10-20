import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Poll, Question, Answer, only_characters_validator
from accounts.models import CustomUser


def create_user():
    user = CustomUser(
            username='test',
            password='testpassword',
            email='test@example.com'
    )
    return user


def create_poll(user):
    poll = Poll(
        user=user,
        name='test',
        description='test description',
        creation_date=timezone.now()
    )
    return poll


def create_question(poll):
    question = Question(
        poll=poll,
        text='test question',
        creation_date=timezone.now()
    )
    return question
        

class PollModelTests(TestCase):
    def setUp(self):
        pass
        #user = create_user()
        #create_poll(user)
        
    def test_was_published_recently_with_future_poll(self):
        '''
            This function returns false for polls whose creation_date
            is in the future
        '''
        current_time = timezone.now()
        user = create_user()
        future_poll = create_poll(user)
        future_poll.creation_date = timezone.now() + timezone.timedelta(days=1)
        self.assertIs(future_poll.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
            This function  returns False for questions whose pub_date
            is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        user = create_user()
        old_poll = create_poll(user)
        old_poll.creation_date = time
        self.assertIs(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
            This function  returns True for questions whose pub_date
            is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        user = create_user()
        recent_poll = create_poll(user)
        recent_poll.creation_date = time
        self.assertIs(recent_poll.was_published_recently(), True)
    
    def test_allowed_characters_to_name(self):
        '''
            This function returns true for allowed characters to poll's name
        '''
        user = create_user()
        poll = create_poll(user)
        poll.name = 'This a valid name'
        self.assertIs(only_characters_validator(poll.name), None)
        poll.name = 'frutas ricas en vitamina c'
        self.assertIs(only_characters_validator(poll.name), None)
        poll.name = 'LENGUAJE DE PROGRAMACION FAVORITO'
        self.assertIs(only_characters_validator(poll.name), None)
    
    def test_not_allowed_characters_to_name(self):
        '''
            This function returns true for not allowed characters to poll's name
        '''
        try:
            user = create_user()
            poll = create_poll(user)
            poll.name = 'This_is_not_valid_name'
            self.assertIs(only_characters_validator(poll.name), ValidationError('This text is not valid'))
        except ValidationError:
            pass
        try:
            poll.name = 'Tipo de bases de *datos'
            self.assertIs(only_characters_validator(poll.name), ValidationError('This text is not valid'))
        except ValidationError:
            pass
        try:
            poll.name = '¿Cual es tu paradigma favorito?'
            self.assertIs(only_characters_validator(poll.name), ValidationError('This text is not valid'))
        except ValidationError:
            pass
    
    def test_allowed_characters_to_description(self):
        '''
            This function returns true for allowed characters to poll's description
        '''
        user = create_user()
        poll = create_poll(user)
        poll.description = 'This a valid description'
        self.assertIs(only_characters_validator(poll.description), None)
        poll.description = 'Esta encuesta se trata de los paradigmas de programacion'
        self.assertIs(only_characters_validator(poll.description), None)
        poll.description = 'Encuesta acerca de cuales frutas son mas ricas en vitamina C'
        self.assertIs(only_characters_validator(poll.description), None)

    def test_not_allowed_characters_to_name(self):
        '''
            This function returns true for not allowed characters to poll's description
        '''
        try:
            user = create_user()
            poll = create_poll(user)
            poll.description = 'This_is_not_valid_description'
            self.assertIs(only_characters_validator(poll.description), ValidationError('This text is not valid'))
        except ValidationError:
            pass
        try:
            poll.description = 'encuesta sobre los tipos de bases de *datos'
            self.assertIs(only_characters_validator(poll.description), ValidationError('This text is not valid'))
        except ValidationError:
            pass
        try:
            poll.description = 'los frameworks web mas\ famosos'
            self.assertIs(only_characters_validator(poll.description), ValidationError('This text is not valid'))
        except ValidationError:
            pass


class PollIndexView(TestCase):
    def test_no_polls(self):
        '''
            If no questions exist, an appropriate message is displayed.
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])


class PollDetailViewTest(TestCase):
    def test_no_questions(self):
        '''
            If no questions exist, an appropriate message is displayed.
        '''
        user = create_user()
        user.save()
        current_time = timezone.now()
        poll = create_poll(user)
        poll.save()
        response = self.client.get(reverse('polls:poll_detail', args=(poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No questions are available.')
        self.assertQuerysetEqual(response.context['poll'].question_set.all(), [])


class QuestionDetailViewTest(TestCase):
    def test_no_questions(self):
        '''
            If no questions exist, an appropriate message is displayed.
        '''
        user = create_user()
        user.save()
        current_time = timezone.now()
        poll = create_poll(user)
        poll.save()
        question = create_question(poll)
        question.save()
        response = self.client.get(reverse('polls:question_detail', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No answers are available.')
        self.assertQuerysetEqual(response.context['question'].answer_set.all(), [])

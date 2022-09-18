from asyncio.base_futures import _future_repr_info
import datetime
from venv import create

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Poll, Question, Answer
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

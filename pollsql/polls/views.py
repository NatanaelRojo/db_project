from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Poll, Question, Answer


#def index(request):
#    latest_poll_list = Poll.objects.order_by('-creation_date')[:5]
 #   context = {'latest_poll_list': latest_poll_list}
  #  return render(request, 'polls/index.html', context)


#def poll_detail(request, poll_id):
    #poll = get_object_or_404(Poll, pk=poll_id)
    #context = {'poll': poll}
#    return render(request, 'polls/poll_detail.html', context)


#def question_detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    context = {'question': question}
#    return render(request, 'polls/question_detail.html', context)

#def results(request, question_id):
 #   question = get_object_or_404(Question, pk=question_id)
  #  context = {'question': question}
   # return render(request, 'polls/results.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.order_by('-creation_date')[:5]


class PollDetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/poll_detail.html'


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'polls/question_detail.html'


class QuestionResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_answer = question.answer_set.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/question_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_answer.votes += 1
        selected_answer.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
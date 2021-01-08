from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'voting/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'voting/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'voting/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'voting/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('voting:results', args=(question.id,)))




def genquestion(request):
    #greate a new question and save into DB
    newquestion = Question(question_text="", pub_date=timezone.now())
    newquestion.save()

    return HttpResponseRedirect(reverse('voting:new', args=(newquestion.id,)))


def new(request, pk):
    #greate a new question and save into DB
    question = get_object_or_404(Question, pk=pk)

    #newquestion = Question(question_text="", pub_date=timezone.now())
    #newquestion.save()

    return render(request, 'voting/new.html', {'pk': pk, 'question': question})

def addtext(request, pk):
    #adds question text
    question = get_object_or_404(Question, pk=pk)
    #TODO get question text and add it to question
    question.question_text = request.POST['text']
    question.save()

    #TODO add redirect to same page with the question text
    return HttpResponseRedirect(reverse('voting:new', args=(pk,)))



def addchoice(request, pk):
    #adds a single question choice
    question = get_object_or_404(Question, pk=pk)
    #TODO add choice to question
    newchoice = Choice(question=question, choice_text=request.POST['choicetext'])
    newchoice.save()

    #TODO redirect to same page
    return HttpResponseRedirect(reverse('voting:new', args=(pk,)))

    


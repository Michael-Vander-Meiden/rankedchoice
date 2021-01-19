from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Choice, Question, RankedVote


class IndexView(generic.ListView):
    template_name = 'voting/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'voting/detail.html'

#TODO fix template so that it shows the accurate ranked choice layout
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'voting/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)
    choices_dict = {}
    ranks_dict = {}
    for i, choice in enumerate(choices):
        choices_dict[choice.id] = 0
        ranks_dict[str(i+1)] = 0

    ranks = [(key.split("_")[1], value) for key, value in request.POST.items() if "choiceid" in key]
    
    for choiceid, rank in ranks:
        
        choices_dict[choiceid] = 1
        ranks_dict[rank] = 1

    # This loop checks to make sure that the keys are in order
    for key, value in ranks_dict.items():
        if value == 0:
            return render(request, 'voting/detail.html', {
                'question': question,
                'error_message': "Make sure you number choices correctly",
            })
    
    for vote in ranks:
        pk = vote[0]
        rank = vote[1]

        cur_choice = Choice.objects.get(pk=pk)
        new_rankedvote = RankedVote(choice=cur_choice, rank=int(rank))
        new_rankedvote.save()

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

    


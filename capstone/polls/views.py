from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions, and
        exclude any questions that aren't yet published.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question": question,
            "error_message": "Please select a choice."
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # returning an HttpResponseRedirect prevent duplicates if back button clicked
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

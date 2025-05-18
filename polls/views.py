from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Question, Choice
from django.db.models import F
from django.views import generic


# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsListView(generic.ListView):
    model = Question
    template_name = "polls/results-list.html"
    context_object_name = "results"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Пожалуйста выберите вопрос",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return redirect("results_page", pk=question_id)


def results(request):
    return render(request, "polls/index.html")

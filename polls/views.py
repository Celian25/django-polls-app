from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Question, Choice
from django.db.models import F
from django.views import generic, View
from django.utils import timezone


# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsListView(View):
    def _calculate_response_obj(self):
        response_obj = {}
        for item in range(1, Question.count_questions() + 1):
            question = Question.objects.get(id=item)
            answers = question.choices.all()

            response_obj[question.question_text] = [
                {"title": ans.choice_text, "votes": ans.votes} for ans in answers
            ]
        return response_obj

    def get(self, request, *args, **kwargs):
        response_obj = self._calculate_response_obj()
        return render(
            request, "polls/results-list.html", context={"data": response_obj}
        )


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

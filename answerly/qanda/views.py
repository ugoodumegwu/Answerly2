from django.shortcuts import render
from django.views import View
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DayArchiveView, RedirectView, DeleteView
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse_lazy


class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'qanda/ask.html'

    def get_initial(self):
        return {
            'user': self.request.user.id,
        }

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        elif action == 'PREVIEW':
            preview = Question(
                question=form.cleaned_data['question'],
                title = form.cleaned_data['title']
            )
            print(form.cleaned_data)
            ctx = self.get_context_data(preview=preview)
            print('inside form valid')
            return render(self.request, self.template_name, ctx)
        return HttpResponseBadRequest()



class QuestionDetailView(DetailView):

    model = Question
    template_name = 'qanda/question_detail.html'

    ACCEPT_FORM = AnswerAcceptanceForm(initial={'accepted': True})
    REJECT_FORM = AnswerAcceptanceForm(initial={'accepted': False})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['answer_form'] = AnswerForm(initial={
            'user' : self.request.user.id,
            'question': self.object.id,
        })
        if self.object.can_accept_answers(self.request.user):
            ctx['accept_form'] = self.ACCEPT_FORM
            ctx['reject_form'] = self.REJECT_FORM
        if self.object.can_delete(self.request.user):
            ctx['delete'] = True
        return ctx


class CreateAnswerView(LoginRequiredMixin, CreateView):

    model = Answer
    form_class = AnswerForm
    template_name = 'qanda/create_answer.html'


    def get_question(self):
        return Question.objects.get(pk=self.kwargs['pk'])

    def get_initial(self):
        ctx = super().get_initial()
        ctx['user'] = self.request.user.id
        ctx['question'] = self.get_question().id
        return ctx

    def get_context_data(self, **kwargs):
        return super().get_context_data(question=self.get_question(), **kwargs)

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == "SAVE":
            return super().form_valid(form)
        elif action == "PREVIEW":
            ctx = self.get_context_data()
            ctx['preview'] = form.cleaned_data['answer']
            return render(self.request, self.template_name, ctx)
        return HttpResponseBadRequest()

    def form_invalid(self, form):
        return super().form_invalid(form)


class UpdateAnswerAcceptanceView(LoginRequiredMixin, UpdateView):

    form_class = AnswerAcceptanceForm
    queryset = Answer.objects.all()

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_invalid(self, form):
        return HttpResponseRedirect(redirect_to=self.object.question.get_absolute_url())


class DailyQuestionListView(DayArchiveView):
    queryset = Question.objects.all()
    date_field = 'created_on'
    month_format = '%m'
    allow_empty = True


class TodaysQuestionList(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        today = timezone.now()
        return reverse('qanda:daily_questions_list',
                       kwargs={
                           'day': today.day,
                           'month': today.month,
                           'year': today.year
                       }
                       )

class DeleteQuestion(DeleteView):

    model = Question
    template_name = 'qanda/question_delete.html'
    success_url = reverse_lazy('qanda:daily_questions')
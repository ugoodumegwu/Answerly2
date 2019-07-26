from django.urls import path
from .views import *


app_name = 'qanda'
urlpatterns = [
    path('ask/', AskQuestionView.as_view(), name='ask'),
    path('q/<int:pk>', QuestionDetailView.as_view(), name='question_detail'),
    path('q/<int:pk>/answer/', CreateAnswerView.as_view(), name='answer_question'),
    path('a/<int:pk>/accept/', UpdateAnswerAcceptanceView.as_view(), name='update_answer_acceptance'),
    path('daily/', TodaysQuestionList.as_view(), name='daily_questions'),
    path('daily/<int:year>/<int:month>/<int:day>', DailyQuestionListView.as_view(), name='daily_questions_list'),
    path('delete/<int:pk>', DeleteQuestion.as_view(), name='delete_question'),
]
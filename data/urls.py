from django.urls import path

from data.views import DataView, ResultView

app_name = 'data'

urlpatterns = [
    path('', DataView.as_view(), name='index'),
    path('<str:uuid>/', ResultView.as_view(), name='result'),
]
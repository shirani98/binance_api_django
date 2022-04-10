from django.shortcuts import render
from django.views.generic import View
from data.forms import DataForm
from data.models import Data


class DataView(View):

    def get(self, request):
        return render(request, 'data/index.html', {'form': DataForm})

    def post(self, request):
        return Data.create_data(self)


class ResultView(View):

    def get(self, request, *args, **kwargs):
        Data.get_result(self.kwargs['uuid'])
        return render(self.request, 'data/result.html')

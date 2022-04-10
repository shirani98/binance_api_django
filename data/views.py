from django.shortcuts import redirect, render
from django.views.generic import View
from decimal import Decimal
from binance.client import Client
from data.forms import DataForm
from data.models import Data, Result


class DataView(View):

    def get(self, request):
        return render(request, 'data/index.html', {'form': DataForm})

    def post(self, request):
        return Data.create_data(self)


class ResultView(View):

    def get(self, request, *args, **kwargs):
        Result.get_result(self.kwargs['uuid'])
        return render(self.request, 'data/result.html', {'Result': Result.objects.filter(data__uuid=self.kwargs['uuid'])})

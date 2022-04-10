from pyexpat import model
from sqlite3 import Timestamp
from django.db import models
from binance.client import Client
from decimal import Decimal
import redis
from django.shortcuts import redirect, render
import uuid

from data.forms import DataForm
# Create your models here.
r = redis.Redis(host='localhost', port=6379, db=0)
client = Client()


class Data(models.Model):
    uuid = models.UUIDField(max_length=10, default=uuid.uuid4, editable=False)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    channel_name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return F"{self.symbol} > {self.price}"

    @classmethod
    def create_data(cls, self):
        form = DataForm(self.request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            price = form.cleaned_data['price']
            channel_name = form.cleaned_data['channel_name']
            query = Data.objects.create(
                symbol=symbol, price=price, channel_name=channel_name)
            return redirect('data:result', query.uuid)
        return redirect('data:index')


class Result(models.Model):
    status_choices = (('up', 'Up'), ('down', 'Down'))

    status = models.CharField(max_length=4, choices=status_choices)
    timestamp = models.CharField(max_length=50)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.ForeignKey(Data, related_name="data",
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_result(cls, data_uuid):
        data = Data.objects.get(uuid=data_uuid)
        klines = client.get_klines(
            symbol=data.symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
        close_price = Decimal(klines[0][4])
        close_time = klines[0][6]
        target_price = Decimal(data.price)
        if close_price > target_price:
            if not cls.objects.filter(data_id=data.id, timestamp=close_time).exists():
                r.publish(data.channel_name, "Down in " +
                          str(close_time) + "time")
                cls.objects.create(
                    status='down', timestamp=close_time, data=data, close_price=close_price)
        elif close_price < target_price:
            if not cls.objects.filter(data_id=data.id, timestamp=close_time).exists():
                r.publish(data.channel_name, " Up in " +
                          str(close_time) + "time")
                cls.objects.create(
                    status='up', timestamp=close_time, data=data, close_price=close_price)

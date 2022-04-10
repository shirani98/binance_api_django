from django.db import models
from binance.client import Client
from decimal import Decimal
import redis
from django.shortcuts import redirect, render
import uuid
from datetime import datetime, timedelta
from data.forms import DataForm
# Create your models here.
r = redis.Redis(host='localhost', port=6379, db=0)
client = Client()

class ArchiveData(models.Model):
    symbol = models.CharField(max_length=10)
    close_time = models.BigIntegerField()
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    
    
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
            query = cls.objects.create(
                symbol=symbol, price=price, channel_name=channel_name)
            return redirect('data:result', query.uuid)
        return redirect('data:index')

    @classmethod
    def get_result(cls, data_uuid):
        data = cls.objects.get(uuid=data_uuid)
        time = datetime.now() - timedelta(minutes=1)
        
        if ArchiveData.objects.filter(symbol=data.symbol, created__gt=time).exists():
            obj = ArchiveData.objects.get(symbol=data.symbol, created__gt=time)
            close_price = obj.close_price
            close_time = obj.close_time
            
        else :
            klines = client.get_klines(symbol=data.symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
            close_price = Decimal(klines[0][4])
            close_time = klines[0][6]
            ArchiveData.objects.create(symbol= data.symbol, close_time = close_time, close_price = close_price)
            
        target_price = Decimal(data.price)
        if close_price > target_price:
            r.publish(data.channel_name, "Down in " + str(close_time) + "time")
        elif close_price < target_price:
            r.publish(data.channel_name, " Up in " + str(close_time) + "time")

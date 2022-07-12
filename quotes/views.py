#from email import message
from termios import TIOCPKT_FLUSHREAD
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from django.template.defaulttags import register

# Create your views here.
# pk_40f41830cd17488cb06e00eebec9b2d6

def home(request):
    import requests
    import json

    if request.method == 'POST':

        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_40f41830cd17488cb06e00eebec9b2d6")
        try:
            api = json.loads(api_request.content)

        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {"api": api})
    
    else:
        return render(request, 'home.html', {"ticker":"Enter a ticker symbol above..."})

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    import requests
    import json
    var1 = 1
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added!"))
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:

            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) +"/quote?token=pk_40f41830cd17488cb06e00eebec9b2d6")
            try:
                api = json.loads(api_request.content)
                output.append(api)

            except Exception as e:
                api = "Error..."
                
        str_list = []
        for i in ticker:
            str_list.append(str(i))

        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output, 'range': range(0,len(ticker)), 'str_list': str_list})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted!"))
    return redirect(add_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})

@register.filter
def index(indexable, i):
    return indexable[i]


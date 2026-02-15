from django.shortcuts import render
from .models import Ticker

def ticker_list(request):
    # Получаем все тикеры из базы
    tickers = Ticker.objects.all()
    
    # Статистика
    total_count = tickers.count()
    
    context = {
        'tickers': tickers,
        'total_count': total_count,
    }
    return render(request, 'market/index.html', context)
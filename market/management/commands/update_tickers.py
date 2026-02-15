from django.core.management.base import BaseCommand
from market.models import Ticker
import requests
from datetime import datetime

class Command(BaseCommand):
    help = 'Загружает тикеры с Bybit API в базу данных'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Начинаем загрузку данных с Bybit...")
        
        url = "https://api.bybit.com/v5/market/tickers"
        params = {'category': 'spot'}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('retCode') != 0:
                self.stderr.write(self.style.ERROR(f"Ошибка API: {data.get('retMsg')}"))
                return

            tickers_list = data.get('result', {}).get('list', [])
            count = 0
            
            for item in tickers_list:
                # Вспомогательная функция для безопасного получения чисел
                def get_float(key):
                    val = item.get(key)
                    if not val or val == "":
                        return None
                    try:
                        return float(val)
                    except ValueError:
                        return None

                # Вычисляем процент изменения
                last_price = get_float('lastPrice') or 0
                prev_price = get_float('prevPrice24h') or 0
                
                if prev_price > 0:
                    change_pcnt = ((last_price - prev_price) / prev_price) * 100
                else:
                    change_pcnt = 0

                # Обновляем или создаем запись
                obj, created = Ticker.objects.update_or_create(
                    symbol=item['symbol'],
                    defaults={
                        'bid_price': get_float('bid1Price'),
                        'ask_price': get_float('ask1Price'),
                        'last_price': last_price if last_price else None,
                        'prev_price_24h': prev_price if prev_price else None,
                        'price_24h_pcnt': change_pcnt,
                        'high_price_24h': get_float('highPrice24h'),
                        'low_price_24h': get_float('lowPrice24h'),
                        'volume_24h': get_float('volume24h'),
                        'turnover_24h': get_float('turnover24h'),
                        'usd_index_price': get_float('usdIndexPrice'),
                        'category': 'spot'
                    }
                )
                if created:
                    count += 1
            
            self.stdout.write(self.style.SUCCESS(f'✅ Успешно обработано {len(tickers_list)} тикеров. Новых: {count}'))
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Ошибка: {e}'))
# update_market_data.py
import requests
import json
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
import html

# Загружаем переменные окружения
load_dotenv()

class BybitDataUpdater:
    def __init__(self):
        self.api_key = os.getenv('BYBIT_API_KEY')
        self.secret_key = os.getenv('BYBIT_SECRET_KEY')
        self.base_url = "https://api.bybit.com"
        
    def get_market_data(self):
        """Получает данные рынка с Bybit API"""
        try:
            # Используем публичный endpoint для получения рыночных данных
            url = f"{self.base_url}/v5/market/tickers"
            
            headers = {
                'X-BAPI-API-KEY': self.api_key,
                'X-BAPI-SIGN-TYPE': "2",  # ← ИСПРАВЛЕНО: строка вместо числа
                'X-BAPI-TIMESTAMP': str(int(datetime.now().timestamp() * 1000)),
                'X-BAPI-RECV-WINDOW': "5000"  # ← ИСПРАВЛЕНО: строка
            }
            
            # Для публичных данных подпись не нужна
            params = {
                'category': 'spot'  # Получаем только спот данные
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('retCode') == 0:
                return data.get('result', {}).get('list', [])
            else:
                print(f"Ошибка API: {data.get('retMsg')}")
                return []
                
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return []
    
    def get_market_data_public(self):
        """Альтернативный способ - полностью публичный запрос без заголовков"""
        try:
            # Полностью публичный endpoint без заголовков
            url = f"{self.base_url}/v5/market/tickers"
            
            params = {
                'category': 'spot',
                'limit': 1000  # Максимум записей
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('retCode') == 0:
                return data.get('result', {}).get('list', [])
            else:
                print(f"Ошибка API: {data.get('retMsg')}")
                return []
                
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return []
    
    def format_market_data(self, api_data):
        """Форматирует данные API в нужный формат"""
        formatted_data = []
        
        for item in api_data:
            # Вычисляем изменение в процентах
            try:
                last_price = float(item.get('lastPrice', 0))
                prev_price = float(item.get('prevPrice24h', 0))
                
                if prev_price > 0:
                    price_change_pcnt = ((last_price - prev_price) / prev_price) * 100
                else:
                    price_change_pcnt = 0
            except (ValueError, TypeError):
                price_change_pcnt = 0
            
            formatted_item = {
                'symbol': item.get('symbol', ''),
                'bid1Price': item.get('bid1Price', ''),
                'bid1Size': item.get('bid1Size', ''),
                'ask1Price': item.get('ask1Price', ''),
                'ask1Size': item.get('ask1Size', ''),
                'lastPrice': item.get('lastPrice', ''),
                'prevPrice24h': item.get('prevPrice24h', ''),
                'price24hPcnt': f"{price_change_pcnt:.4f}",
                'highPrice24h': item.get('highPrice24h', ''),
                'lowPrice24h': item.get('lowPrice24h', ''),
                'turnover24h': item.get('turnover24h', ''),
                'volume24h': item.get('volume24h', ''),
                'usdIndexPrice': '',  # Bybit не предоставляет этот индекс
                'category': 'spot'
            }
            
            formatted_data.append(formatted_item)
        
        return formatted_data
    
    def save_to_csv(self, data, filename='market_data.csv'):
        """Сохраняет данные в CSV файл"""
        if not data:
            print("Нет данных для сохранения")
            return False
            
        fieldnames = [
            'symbol', 'bid1Price', 'bid1Size', 'ask1Price', 'ask1Size',
            'lastPrice', 'prevPrice24h', 'price24hPcnt', 'highPrice24h',
            'lowPrice24h', 'turnover24h', 'volume24h', 'usdIndexPrice', 'category'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"✅ Данные сохранены в {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при сохранении CSV: {e}")
            return False
    
    def update_html_table(self):
        """Обновляет HTML таблицу с новыми данными"""
        print("🔄 Получение данных с Bybit API...")
        
        # Пробуем сначала публичный способ
        api_data = self.get_market_data_public()
        
        # Если публичный способ не сработал, пробуем с API ключами
        if not api_data and self.api_key:
            print("🔑 Пробуем с API ключами...")
            api_data = self.get_market_data()
        
        if not api_data:
            print("❌ Не удалось получить данные")
            return False
        
        print(f"📊 Получено {len(api_data)} торговых пар")
        
        # Форматируем данные
        formatted_data = self.format_market_data(api_data)
        
        # Сохраняем в CSV
        if self.save_to_csv(formatted_data):
            # Обновляем HTML таблицу
            print("🔄 Обновление HTML таблицы...")
            try:
                # Импортируем функцию из generate_market_table
                import sys
                sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                from generate_market_table import generate_html_table
                
                generate_html_table()
                print("✅ HTML таблица обновлена!")
                return True
                
            except Exception as e:
                print(f"❌ Ошибка при обновлении HTML: {e}")
                return False
        else:
            return False

def main():
    print("🚀 Обновление данных Bybit API")
    print("=" * 50)
    
    updater = BybitDataUpdater()
    
    # Проверяем API ключи (необязательно для публичных данных)
    print(f"🔑 API ключ: {'✅ Установлен' if updater.api_key else '❌ Не установлен (будем использовать публичные данные)'}")
    
    # Обновляем данные
    success = updater.update_html_table()
    
    if success:
        print("=" * 50)
        print("✅ Обновление завершено успешно!")
        print("🌐 Откройте market_data_table.html для просмотра обновленных данных")
    else:
        print("❌ Ошибка при обновлении данных")

if __name__ == "__main__":
    main()
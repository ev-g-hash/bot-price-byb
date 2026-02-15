# generate_market_table.py
import csv
import html
import os

def generate_html_table():
    """Генерирует HTML таблицу из CSV файла с выбранными столбцами"""
    
    # Проверяем наличие CSV файла
    if not os.path.exists('market_data.csv'):
        print("Файл market_data.csv не найден!")
        return
    
    # Читаем CSV файл
    with open('market_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    
    print(f"Загружено {len(data)} торговых пар")
    
    # Начинаем создавать HTML
    html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Рыночные данные криптовалют</title>
    <link rel="stylesheet" href="market_styles.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>📊 Рыночные данные криптовалют</h1>
            <div class="stats">
                <span class="stat-item">
                    <span class="stat-label">Всего пар:</span>
                    <span class="stat-value" id="totalCount">''' + str(len(data)) + '''</span>
                </span>
                <span class="stat-item">
                    <span class="stat-label">Показано:</span>
                    <span class="stat-value" id="visibleCount">''' + str(len(data)) + '''</span>
                </span>
            </div>
        </header>
        
        <div class="controls">
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="🔍 Поиск по торговой паре..." class="search-input">
            </div>
            <div class="filter-container">
                <select id="categoryFilter" class="filter-select">
                    <option value="">📂 Все категории</option>
                    <option value="spot">💰 Spot</option>
                </select>
            </div>
            <div class="sort-container">
                <button id="sortBtn" class="sort-btn">🔄 Сортировка по изменению</button>
            </div>
        </div>

        <div class="table-wrapper">
            <table id="marketTable" class="market-table">
                <thead>
                    <tr>
                        <th data-column="symbol" class="sortable">📈 Торговая пара</th>
                        <th data-column="bid1Price" class="sortable">💵 Цена покупки</th>
                        <th data-column="ask1Price" class="sortable">💸 Цена продажи</th>
                        <th data-column="prevPrice24h" class="sortable">📊 Цена за 24ч</th>
                        <th data-column="price24hPcnt" class="sortable">📈 Изменение 24ч (%)</th>
                        <th data-column="highPrice24h" class="sortable">⬆️ Максимум 24ч</th>
                        <th data-column="lowPrice24h" class="sortable">⬇️ Минимум 24ч</th>
                        <th data-column="turnover24h" class="sortable">💰 Оборот 24ч</th>
                        <th data-column="volume24h" class="sortable">📦 Объем 24ч</th>
                        <th data-column="usdIndexPrice" class="sortable">💲 USD индекс</th>
                        <th data-column="category">📂 Категория</th>
                    </tr>
                </thead>
                <tbody id="tableBody">'''
    
    # Генерируем строки таблицы
    for i, row in enumerate(data):
        # Определяем класс для изменения цены
        try:
            price_change = float(row.get('price24hPcnt', 0) or 0)
        except (ValueError, TypeError):
            price_change = 0
            
        change_class = 'positive' if price_change > 0 else 'negative' if price_change < 0 else 'neutral'
        change_text = f"+{price_change:.2f}%" if price_change > 0 else f"{price_change:.2f}%"
        
        # Экранируем HTML для безопасности
        symbol = html.escape(row.get('symbol', ''))
        bid1Price = html.escape(row.get('bid1Price', ''))
        ask1Price = html.escape(row.get('ask1Price', ''))
        prevPrice24h = html.escape(row.get('prevPrice24h', ''))
        highPrice24h = html.escape(row.get('highPrice24h', ''))
        lowPrice24h = html.escape(row.get('lowPrice24h', ''))
        turnover24h = html.escape(row.get('turnover24h', ''))
        volume24h = html.escape(row.get('volume24h', ''))
        usdIndexPrice = html.escape(row.get('usdIndexPrice', ''))
        category = html.escape(row.get('category', ''))
        
        html_content += f'''
                    <tr class="data-row" data-index="{i}">
                        <td class="symbol-cell"><strong>{symbol}</strong></td>
                        <td class="price-cell">{bid1Price}</td>
                        <td class="price-cell">{ask1Price}</td>
                        <td class="price-cell">{prevPrice24h}</td>
                        <td class="change-cell {change_class}">{change_text}</td>
                        <td class="price-cell">{highPrice24h}</td>
                        <td class="price-cell">{lowPrice24h}</td>
                        <td class="volume-cell">{turnover24h}</td>
                        <td class="volume-cell">{volume24h}</td>
                        <td class="price-cell">{usdIndexPrice}</td>
                        <td class="category-cell">{category}</td>
                    </tr>'''
    
    # Завершаем HTML
    html_content += '''
                </tbody>
            </table>
        </div>
        
        <div class="loading" id="loadingIndicator" style="display: none;">
            <div class="spinner"></div>
            <span>Загрузка данных...</span>
        </div>
    </div>

    <script src="market_script.js"></script>
</body>
</html>'''
    
    # Сохраняем HTML файл
    with open('market_data_table.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print("✅ HTML файл 'market_data_table.html' создан успешно!")
    print(f"📊 Добавлено {len(data)} торговых пар")
    
    # Создаем файл с данными для JavaScript
    create_data_file(data)

def create_data_file(data):
    """Создает JavaScript файл с данными"""
    js_content = "// Данные торговых пар для JavaScript\nconst marketData = [\n"
    
    for row in data:
        js_content += "    {\n"
        js_content += f"        symbol: '{row.get('symbol', '')}',\n"
        js_content += f"        bid1Price: '{row.get('bid1Price', '')}',\n"
        js_content += f"        ask1Price: '{row.get('ask1Price', '')}',\n"
        js_content += f"        prevPrice24h: '{row.get('prevPrice24h', '')}',\n"
        js_content += f"        price24hPcnt: '{row.get('price24hPcnt', '')}',\n"
        js_content += f"        highPrice24h: '{row.get('highPrice24h', '')}',\n"
        js_content += f"        lowPrice24h: '{row.get('lowPrice24h', '')}',\n"
        js_content += f"        turnover24h: '{row.get('turnover24h', '')}',\n"
        js_content += f"        volume24h: '{row.get('volume24h', '')}',\n"
        js_content += f"        usdIndexPrice: '{row.get('usdIndexPrice', '')}',\n"
        js_content += f"        category: '{row.get('category', '')}'\n"
        js_content += "    },\n"
    
    js_content += "];\n"
    
    with open('market_data.js', 'w', encoding='utf-8') as file:
        file.write(js_content)
    
    print("✅ JavaScript файл с данными 'market_data.js' создан!")

if __name__ == "__main__":
    print("🚀 Генерация HTML таблицы с рыночными данными...")
    print("=" * 50)
    
    # Генерируем основной HTML файл
    generate_html_table()
    
    print("=" * 50)
    print("✅ Все файлы созданы успешно!")
    print("\n📁 Созданные файлы:")
    print("   📄 market_data_table.html - основная HTML страница")
    print("   🎨 market_styles.css - стили оформления")
    print("   ⚡ market_script.js - интерактивность")
    print("   📊 market_data.js - данные для JavaScript")
    print("\n🌐 Откройте market_data_table.html в браузере!")
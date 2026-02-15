// market_script.js
// Глобальные переменные
let currentData = [];
let originalData = [];
let sortDirection = 'desc';
let currentSortColumn = 'price24hPcnt';

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeTable();
    setupEventListeners();
});

function initializeTable() {
    const tableBody = document.getElementById('tableBody');
    const rows = tableBody.getElementsByClassName('data-row');
    
    // Сохраняем данные в массив для сортировки
    currentData = Array.from(rows).map((row, index) => {
        return {
            element: row,
            index: index,
            symbol: row.cells[0].textContent.trim(),
            bid1Price: parseFloat(row.cells[1].textContent) || 0,
            ask1Price: parseFloat(row.cells[2].textContent) || 0,
            prevPrice24h: parseFloat(row.cells[3].textContent) || 0,
            price24hPcnt: parseFloat(row.cells[4].textContent.replace('%', '')) || 0,
            highPrice24h: parseFloat(row.cells[5].textContent) || 0,
            lowPrice24h: parseFloat(row.cells[6].textContent) || 0,
            turnover24h: parseFloat(row.cells[7].textContent) || 0,
            volume24h: parseFloat(row.cells[8].textContent) || 0,
            usdIndexPrice: parseFloat(row.cells[9].textContent) || 0,
            category: row.cells[10].textContent.trim()
        };
    });
    
    originalData = [...currentData];
    updateVisibleCount();
}

function setupEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const sortBtn = document.getElementById('sortBtn');
    const tableHeaders = document.querySelectorAll('.market-table th.sortable');

    // Поиск
    searchInput.addEventListener('input', filterTable);
    
    // Фильтр по категории
    categoryFilter.addEventListener('change', filterTable);
    
    // Кнопка сортировки
    sortBtn.addEventListener('click', toggleSort);
    
    // Сортировка по заголовкам
    tableHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.column;
            sortByColumn(column);
        });
    });
}

function filterTable() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const categoryValue = document.getElementById('categoryFilter').value;
    const rows = document.getElementsByClassName('data-row');
    let visibleCount = 0;

    for (let row of rows) {
        const symbol = row.cells[0].textContent.toLowerCase();
        const category = row.cells[10].textContent;
        
        const matchesSearch = symbol.includes(searchTerm);
        const matchesCategory = !categoryValue || category === categoryValue;
        
        const isVisible = matchesSearch && matchesCategory;
        row.style.display = isVisible ? '' : 'none';
        
        if (isVisible) {
            visibleCount++;
            row.style.animation = 'fadeInUp 0.3s ease-out';
        }
    }
    
    updateVisibleCount(visibleCount);
}

function updateVisibleCount(count = null) {
    const visibleCountElement = document.getElementById('visibleCount');
    const totalCountElement = document.getElementById('totalCount');
    
    if (count === null) {
        const visibleRows = document.querySelectorAll('.data-row[style*="display: none"]').length;
        count = currentData.length - visibleRows;
    }
    
    if (visibleCountElement) {
        visibleCountElement.textContent = count;
    }
    
    if (totalCountElement) {
        totalCountElement.textContent = currentData.length;
    }
}

function sortByColumn(column) {
    // Убираем классы сортировки со всех заголовков
    document.querySelectorAll('.market-table th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Добавляем класс к текущему заголовку
    const currentHeader = document.querySelector(`[data-column="${column}"]`);
    if (currentHeader) {
        if (currentSortColumn === column) {
            sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            sortDirection = 'desc';
            currentSortColumn = column;
        }
        
        currentHeader.classList.add(sortDirection === 'asc' ? 'sort-asc' : 'sort-desc');
    }
    
    // Сортируем данные
    currentData.sort((a, b) => {
        let aVal = a[column];
        let bVal = b[column];
        
        // Специальная обработка для разных типов данных
        if (column === 'symbol' || column === 'category') {
            aVal = aVal.toLowerCase();
            bVal = bVal.toLowerCase();
            if (sortDirection === 'asc') {
                return aVal.localeCompare(bVal);
            } else {
                return bVal.localeCompare(aVal);
            }
        } else {
            // Числовая сортировка
            if (sortDirection === 'asc') {
                return aVal - bVal;
            } else {
                return bVal - aVal;
            }
        }
    });
    
    // Обновляем порядок строк в таблице
    const tableBody = document.getElementById('tableBody');
    currentData.forEach((data, index) => {
        if (data.element.parentNode === tableBody) {
            tableBody.appendChild(data.element);
        }
    });
    
    // Анимация перестановки
    currentData.forEach(data => {
        data.element.style.animation = 'fadeInUp 0.4s ease-out';
    });
}

function toggleSort() {
    const sortBtn = document.getElementById('sortBtn');
    
    if (currentSortColumn === 'price24hPcnt') {
        sortDirection = sortDirection === 'desc' ? 'asc' : 'desc';
        sortBtn.textContent = sortDirection === 'desc' 
            ? '📈 Сортировка по убыванию' 
            : '📉 Сортировка по возрастанию';
    } else {
        currentSortColumn = 'price24hPcnt';
        sortDirection = 'desc';
        sortBtn.textContent = '📈 Сортировка по убыванию';
    }
    
    sortByColumn(currentSortColumn);
}

// Дополнительные функции
function highlightRow(row) {
    row.style.backgroundColor = '#fff3cd';
    row.style.transform = 'scale(1.02)';
    row.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.2)';
    row.style.transition = 'all 0.3s ease';
    
    setTimeout(() => {
        row.style.backgroundColor = '';
        row.style.transform = '';
        row.style.boxShadow = '';
    }, 2000);
}

function exportToCSV() {
    const headers = ['Торговая пара', 'Цена покупки', 'Цена продажи', 'Цена за 24ч', 
                    'Изменение 24ч (%)', 'Максимум 24ч', 'Минимум 24ч', 
                    'Оборот 24ч', 'Объем 24ч', 'USD индекс', 'Категория'];
    
    let csvContent = headers.join(',') + '\\n';
    
    currentData.forEach(data => {
        const row = [
            data.symbol,
            data.bid1Price,
            data.ask1Price,
            data.prevPrice24h,
            data.price24hPcnt + '%',
            data.highPrice24h,
            data.lowPrice24h,
            data.turnover24h,
            data.volume24h,
            data.usdIndexPrice,
            data.category
        ];
        csvContent += row.join(',') + '\\n';
    });
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'market_data_filtered.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Функция для обновления данных (можно вызвать для получения новых данных)
function refreshData() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.style.display = 'flex';
    
    // Имитация загрузки новых данных
    setTimeout(() => {
        // Здесь можно добавить логику обновления данных
        console.log('Данные обновлены');
        loadingIndicator.style.display = 'none';
        
        // Пересоздаем таблицу с новыми данными
        location.reload();
    }, 1500);
}

// Клавиатурные сокращения
document.addEventListener('keydown', function(event) {
    // Ctrl+F для фокуса на поиск
    if (event.ctrlKey && event.key === 'f') {
        event.preventDefault();
        document.getElementById('searchInput').focus();
    }
    
    // Escape для очистки поиска
    if (event.key === 'Escape') {
        document.getElementById('searchInput').value = '';
        filterTable();
        document.getElementById('searchInput').blur();
    }
});

// Добавляем обработку кликов по строкам для детальной информации
document.addEventListener('click', function(event) {
    const row = event.target.closest('.data-row');
    if (row && event.target.closest('.symbol-cell')) {
        const symbol = row.cells[0].textContent;
        console.log(`Клик по торговой паре: ${symbol}`);
        highlightRow(row);
    }
});
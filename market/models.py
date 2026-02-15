from django.db import models

class Ticker(models.Model):
    symbol = models.CharField(max_length=50, unique=True, verbose_name="Торговая пара")
    bid_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Цена покупки")
    ask_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Цена продажи")
    last_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Последняя цена")
    prev_price_24h = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Цена 24ч назад")
    price_24h_pcnt = models.DecimalField(max_digits=10, decimal_places=4, default=0, verbose_name="Изменение 24ч (%)")
    high_price_24h = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Максимум 24ч")
    low_price_24h = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="Минимум 24ч")
    volume_24h = models.DecimalField(max_digits=30, decimal_places=8, null=True, blank=True, verbose_name="Объем 24ч")
    turnover_24h = models.DecimalField(max_digits=30, decimal_places=8, null=True, blank=True, verbose_name="Оборот 24ч")
    usd_index_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True, verbose_name="USD индекс")
    category = models.CharField(max_length=20, default='spot', verbose_name="Категория")
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        ordering = ['-volume_24h'] # Сортировка по умолчанию
        verbose_name = "Тикер"
        verbose_name_plural = "Тикеры"

    def __str__(self):
        return self.symbol
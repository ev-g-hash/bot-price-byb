from django.contrib import admin
from django.urls import path
from market.views import ticker_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ticker_list, name='ticker_list'),
]
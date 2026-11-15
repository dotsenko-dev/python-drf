"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# include - підключає urls.py з іншого застосунку
# path - створення та опис одного маршруту
from django.urls import include, path

# urlpatterns - список маршрутів, які django шукає в цьому файлі (описано в config/settings.py в ROOT_URLCONF = "config.urls")
# для кожного модуля створюється один маршрут path тут
# django отримує URL із початковим слешем (/pizzas/5), відрізає його і далі зіставляє шлях без нього (pizzas/5)
# django перевіряє зверху вниз на збіг з пошукового запиту з url. Якщо перша частина, тут це pizzas, збігається, то django відрізає цей префікс і за допомогою include() передає решту url у дочірній модуль для подальшої перевірки на збіг
# повний шлях = префікс звідси + решта з apps/pizza/urls.py, наприклад "pizzas" + "/5" = pizzas/5 (слеш між pizzas і 5 стоїть у дочірньому файлі, бо тут префікс без кінцевого слеша)
urlpatterns = [path("pizzas", include("apps.pizza.urls"))]

from django.urls import path

# from apps.pizza.views import PizzaListCreateView, PizzaRetrieveUpdateDestroyView
from .views import PizzaListCreateView, PizzaRetrieveUpdateDestroyView

# Цю частину django підключає через include() з config/urls.py: повний шлях = "pizzas" + шлях звідси
urlpatterns = [
    # сюди приходить залишок URL після префікса "pizzas": для /pizzas це ""
    # django для path() очікує функцію (request) -> response, тому as_view() перетворює наш клас на таку функцію. На кожен запит ця функція створює новий екземпляр нашого класу і через dispatch викликає метод (get, post...), що відповідає методу запиту.
    path("", PizzaListCreateView.as_view()),
    # для /pizzas/5 це "/5", тому патерн для однієї піци починається зі слеша: "/<int:pk>"
    # Тут саме "pk" мусить бути, бо ми успадковуємо GenericAPIView, в якому оголошено саме lookup_field = 'pk'. Це можна змінити, якщо змінити lookup_field у нашому класі
    # <int:pk>: int - приймає рядок типу "123" і перетворює його на число. pk - ім'я аргументу, що потрапляє у GenericAPIView і за яким get_object() в GenericAPIView шукає запис
    path("/<int:pk>", PizzaRetrieveUpdateDestroyView.as_view()),
]

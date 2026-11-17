# AppConfig: базовий клас, у якому Django зберігає налаштування застосунку (назва, тип id тощо)
from django.apps import AppConfig


# запис "apps.pizza" в INSTALLED_APPS не вказує клас, тому Django сам шукає його в apps.py і бере єдиний підклас AppConfig, який там є
class PizzaConfig(AppConfig):
    # тип поля id, яке Django додає автоматично в моделі цього застосунку, де первинний ключ не вказано вручну
    # BigAutoField: 64-бітне ціле число з автоінкрементом (до ~9 квінтильйонів записів), AutoField дає лише ~2 мільярди
    default_auto_field = "django.db.models.BigAutoField"

    # python-назва застосунку: повний шлях до його пакета в крапковому записі (як в import apps.pizza)
    # має вказувати на реальну папку з моделями, інакше Django не запуститься
    # остання частина (pizza) стає короткою назвою застосунку: з неї будуються назви таблиць у БД і міграцій
    name = "apps.pizza"

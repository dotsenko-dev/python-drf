from django.db import models

from core.models import BaseModel


# модель - це опис таблиці в БД
# наслідуємо BaseModel, тому до наших полів додаються created_at і updated_at
class PizzaModel(BaseModel):
    # Meta - налаштування самої моделі, а не поля
    class Meta:
        # назва таблиці в БД; без цього django назвав би її за своїм шаблоном
        db_table = "pizza"

    # id (первинний ключ) тут не описано: django сам додає це поле в модель, а значення (1, 2, 3...) видає БД через автоінкремент.
    # саме за цим полем ми шукаємо запис через <int:pk> в urls.py (pk = primary key)

    # CharField - короткий рядок, у БД VARCHAR(20); max_length обов'язковий
    name = models.CharField(max_length=20)
    # IntegerField - ціле число
    size = models.IntegerField()
    # DecimalField - точне десяткове число: max_digits - скільки цифр усього, decimal_places - скільки з них після коми
    price = models.DecimalField(max_digits=10, decimal_places=2)

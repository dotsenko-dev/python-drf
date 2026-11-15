from django.db import models


# спільна основа для всіх моделей проєкту: два службові поля часу описуємо один раз, а не в кожній моделі
class BaseModel(models.Model):  # Створення власної моделі, яку я далі буду наслідувати
    class Meta:
        # абстрактна модель: власної таблиці й міграцій немає, її поля копіюються в таблиці моделей-нащадків (PizzaModel тощо)
        abstract = True

    # auto_now_add: значення ставиться один раз, у момент створення запису, і далі не змінюється
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now: значення оновлюється при кожному збереженні запису (save())
    updated_at = models.DateTimeField(auto_now=True)

    # великий creation_counter ставить ці поля в кінець списку полів моделі, тож у новій таблиці колонки йдуть після власних полів нащадка (для вже створеної таблиці це не працює: нові колонки додаються в кінець)
    created_at.creation_counter = 10**9
    updated_at.creation_counter = 10**9 + 1

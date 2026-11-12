from django.db import models


class BaseModel(models.Model):  # Створення власної моделі, яку я далі буду наслідувати
    class Meta:
        abstract = True  # Інформація для міграцій (не створювати файл міграції для цієї моделі)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Кидаю ці два поля одразу в кінець моделі, щоб не рухати вручну їх потім (правда працює лише для першого створення, потім вони все одно при додаванні нових полів не в кінці будуть)
    created_at.creation_counter = 10**9
    updated_at.creation_counter = 10**9 + 1

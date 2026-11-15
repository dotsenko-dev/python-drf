# serializers - модуль DRF із класами для перетворення даних
from rest_framework import serializers

from apps.pizza.models import PizzaModel


# серіалізатор робить дві речі:
# 1) вихід: перетворює об'єкт моделі на словник, який потім стає JSON
# 2) вхід: перевіряє дані від клієнта (валідація) і створює або оновлює запис
# ModelSerializer будує поля за моделлю й сам реалізує create() та update(),
# тому в ручному варіанті нижче це доводиться писати самому
# [PizzaModel] - лише типізація для mypy, на роботу не впливає
class PizzaSerializer(serializers.ModelSerializer[PizzaModel]):
    class Meta:
        # з якої моделі генеруються поля й правила валідації (max_length, max_digits...)
        model = PizzaModel

        # опис полів, які потрапляють у відповідь і приймаються на вхід. id, created_at, updated_at ModelSerializer сам робить read_only (id - автоматичне поле, created_at/updated_at заповнюють auto_now_add/auto_now), тож клієнт їх не надсилає, лише отримує
        fields = (
            "id",
            "name",
            "size",
            "price",
            "created_at",
            "updated_at",
        )


# Serializer: нічого не знає про модель, кожне поле й правило описуємо руками
# class PizzaSerializer(serializers.Serializer[Any]):

#     # read_only: поле лише віддається клієнту, а з вхідних даних ігнорується (id видає БД, час виставляє модель)
#     id = serializers.IntegerField(read_only=True)

#     #типи й обмеження дублюють модель (max_length=20, max_digits...). Змінимо модель - мусимо змінити й тут
#     name = serializers.CharField(max_length=20)
#     size = serializers.IntegerField()
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     # викликається через serializer.save(), якщо serializer створено без instance (post запит)
#     # validated_data - дані, що пройшли валідацію; ** розпаковує їх в аргументи моделі
#     def create(self, validated_data: dict[str, Any]) -> PizzaModel:
#         return PizzaModel.objects.create(**validated_data)

#     # викликається через serializer.save(), якщо передано instance (put/patch запити) - проходимо по отриманих полях, перезаписуємо його в існуючий об'єкт (setattr) і зберігаємо в БД
#     def update(
#         self, instance: PizzaModel, validated_data: dict[str, Any]
#     ) -> PizzaModel:
#         for k, v in validated_data.items():
#             setattr(instance, k, v)
#         instance.save()
#         return instance

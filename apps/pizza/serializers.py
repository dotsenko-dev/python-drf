from rest_framework import serializers

from apps.pizza.models import PizzaModel


# В ModelSerializer поля створення та оновлення вже вшиті в сам серіалайзер
class PizzaSerializer(
    serializers.ModelSerializer[PizzaModel]
):  # Тут додаю типізацію серіалайзера, бо mypy свариться
    class Meta:
        model = PizzaModel  # З якої моделі брати поля і правила валідації
        fields = (
            "id",
            "name",
            "size",
            "price",
            "created_at",
            "updated_at",
        )  # Тут кажеться, які поля будуть валідуватися та віддаватися клієнту


# from typing import Any

# from rest_framework import serializers

# from apps.pizza.models import PizzaModel


# class PizzaSerializer(serializers.Serializer[Any]):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=20)
#     size = serializers.IntegerField()
#     price = serializers.DecimalField(max_digits=10, decimal_places=2)
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data: dict[str, Any]) -> PizzaModel:
#         return PizzaModel.objects.create(**validated_data)

#     def update(
#         self, instance: PizzaModel, validated_data: dict[str, Any]
#     ) -> PizzaModel:
#         for k, v in validated_data.items():
#             setattr(instance, k, v)
#         instance.save()
#         return instance

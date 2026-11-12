# from django.db.models import QuerySet
# from django.http import QueryDict
# from rest_framework.exceptions import ValidationError

# from apps.pizza.models import PizzaModel


# def filter_pizza(query_params: QueryDict) -> QuerySet:
#     qs = PizzaModel.objects.all()

#     for k, v in query_params.items():
#         match k:
#             # --- price filters ---
#             case "price_eq":
#                 qs = qs.filter(price=v)  # Точний збіг значення
#             case "price_gt":
#                 qs = qs.filter(price__gt=v)  # Більше ніж вказане значення
#             case "price_gte":
#                 qs = qs.filter(price__gte=v)  # Більше або дорівнює вказаному значенню
#             case "price_lt":
#                 qs = qs.filter(price__lt=v)  # Менше ніж вказане значення
#             case "price_lte":
#                 qs = qs.filter(price__lte=v)  # Менше або дорівнює вказаному значенню

#             # --- name filters ---
#             case "name_iexact":
#                 qs = qs.filter(
#                     name__iexact=v
#                 )  # Точний збіг значення без урахування регістру
#             case "name_contains":
#                 qs = qs.filter(name__icontains=v)  # Містить частину слова
#             case "name_startswith":
#                 qs = qs.filter(name__istartswith=v)  # Починається з...

#             # --- size filters ---
#             case "size_eq":
#                 qs = qs.filter(size=v)  # Точний збіг значення
#             case "size_gt":
#                 qs = qs.filter(size__gt=v)  # Більше ніж вказане значення
#             case "size_gte":
#                 qs = qs.filter(size__gte=v)  # Більше або дорівнює вказаному значенню
#             case "size_lt":
#                 qs = qs.filter(size__lt=v)  # Менше ніж вказане значення
#             case "size_lte":
#                 qs = qs.filter(size__lte=v)  # Менше або дорівнює вказаному значенню

#             case _:
#                 raise ValidationError(detail=f"Invalid query parameter: {k}")

#     return qs


from django.core.exceptions import (
    ValidationError as DjangoValidationError,  # Роблю псевдонім, щоб прибрати конфлікти з rest_framework (одна назва)
)
from django.db.models import QuerySet
from django.http import QueryDict
from rest_framework.exceptions import ValidationError

from apps.pizza.models import PizzaModel

# Білий список в URL (ті фільтри, які код обробляє)
ALLOWED_FILTERS = {
    "price_eq": "price",
    "price_gt": "price__gt",
    "price_gte": "price__gte",
    "price_lt": "price__lt",
    "price_lte": "price__lte",
    "name_iexact": "name__iexact",
    "name_contains": "name__icontains",
    "name_startswith": "name__istartswith",
    "size_eq": "size",
    "size_gt": "size__gt",
    "size_gte": "size__gte",
    "size_lt": "size__lt",
    "size_lte": "size__lte",
}


def filter_pizza(query_params: QueryDict) -> QuerySet[PizzaModel]:  # Типізую qs
    qs = (
        PizzaModel.objects.all()
    )  # Початковий QuerySet: усі піци. Запиту до БД ще немає

    for k, v in query_params.items():  # Перебираю поля ключ: значення з params
        if k not in ALLOWED_FILTERS:  # Параметра немає в білому списку
            raise ValidationError(
                {k: [f"Unknown filter. Allowed: {', '.join(ALLOWED_FILTERS)}"]}
            )  # Кидаю помилку 400 з цим текстом

        try:
            qs = qs.filter(
                **{ALLOWED_FILTERS[k]: v}
            )  # розгортаю білий список і ставлю умову фільтра по ключу-значенню
        except DjangoValidationError as e:  # Якщо помилка значень в decimal та дата
            raise ValidationError(
                {k: e.messages}
            )  # Перекидаю повідомлення помилки з django (filter) в DRF
        except ValueError as e:  # Помилка виникає, якщо число мусить бути цілим
            raise ValidationError(
                {k: [str(e)]}
            )  # Кидаю в DRF помилку по стандарту, що і вище
        except Exception:  # Ловлю невраховані помилки
            raise ValidationError({k: ["Invalid value for this parameter."]})

    return qs  # Повертаю створений QuerySet (запиту до БД ще немає)

# Старий варіант: кожен фільтр окремим case в match. Той самий шаблон qs.filter(...) повторюється
# Не ловляться помилки
# Замінено словником ALLOWED_FILTERS
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


# ValidationError з Django (ORM) - його кидає filter(), коли значення не підходить типу поля. Псевдонім потрібен, бо в DRF є клас з такою самою назвою
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.db.models import QuerySet
from django.http import QueryDict

# ValidationError з DRF - з нього DRF сам робить відповідь 400 з текстом помилки
from rest_framework.exceptions import ValidationError

from apps.pizza.models import PizzaModel

# словник дозволених фільтрів:
# ключ - параметр в URL (те, що пише клієнт), значення - умова ORM (те, що розуміє filter()).
# Все, чого тут немає, відхиляється
# суфікси: gt/gte - більше/більше або дорівнює, lt/lte - менше/менше або дорівнює, iexact/icontains/istartswith - збіг/містить/починається з, літера i = без урахування регістру
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


# приймає параметри запиту (?price_gt=100&name_contains=dom), повертає відфільтрований QuerySet;
# викликається з get_queryset у нашому view
def filter_pizza(query_params: QueryDict) -> QuerySet[PizzaModel]:  # Типізую qs
    # початковий QuerySet - усі піци. QuerySet ледачий, запиту до БД ще немає
    qs = PizzaModel.objects.all()

    # перебираємо пари ключ-значення з URL (значення завжди рядки)
    for k, v in query_params.items():
        # невідомий параметр - одразу 400
        if k not in ALLOWED_FILTERS:
            raise ValidationError(
                {k: [f"Unknown filter. Allowed: {', '.join(ALLOWED_FILTERS)}"]}
            )

        try:
            # **{...} розпаковує словник в іменований аргумент:
            # для price_gt=100 це filter(price__gt="100");
            # кілька filter() поспіль звужують результат: у ньому лишаються лише піци, що підходять під усі умови одразу
            # значення перевіряється вже тут, тому помилки типу "abc замість числа" вилітають у filter()
            qs = qs.filter(**{ALLOWED_FILTERS[k]: v})
        # значення не можна перетворити на тип поля (наприклад price=abc для DecimalField)
        except DjangoValidationError as e:
            # перекладаємо помилку django на помилку DRF, щоб клієнт отримав 400, а не 500
            raise ValidationError({k: e.messages})
        # те саме для цілих полів (size=abc)
        except ValueError as e:
            raise ValidationError({k: [str(e)]})
        # страховка на випадок іншої помилки значення
        # недолік: такий перехоплювач може сховати справжню помилку в коді
        except Exception:  # noqa: BLE001
            raise ValidationError({k: ["Invalid value for this parameter."]})

    # повертаємо QuerySet. Запит до БД піде пізніше, коли наш view почне його читати
    return qs

# готові generic-класи DRF: поєднують GenericAPIView з потрібними міксинами
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.pizza.filter import filter_pizza
from apps.pizza.models import PizzaModel
from apps.pizza.serializers import PizzaSerializer

# # APIView - базовий клас DRF: сам лише приймає запит і викликає метод (get, post...)
# # усе інше пишемо руками

# class PizzaListCreateView(APIView):
#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         # Приклади роботи з ORM (кожен перезаписує попередній, додавши до нього новий фільтр):

#         # filter з Q: (розмір > 5 або назва domino1) і ціна > 10
#         # Q потрібен для "або" (|), зі звичайними умовами поєднується, якщо Q іде першим
#         # exclude - прибрати з вибірки піци розміром 78
#         # order_by("size", "-price") - сортування за розміром, а при однаковому розмірі - за ціною спаданням
#         # reverse() - розвернути порядок
#         # pizzas = (PizzaModel.objects.filter(Q(size__gt=5) | Q(name="domino1"), price__gt=10)
#         #           .exclude(size=78).order_by("size", "-price").reverse())

#         # зріз зі кроком [1:6:2] -> індекси 1, 3, 5, з кроком запит до БД іде одразу
#         # без кроку [1:6] QuerySet лишається ледачим
#         # pizzas = PizzaModel.objects.all()[1:6:2]

#         # values - замість об'єктів моделі словники з вказаними полями
#         # pizzas = PizzaModel.objects.all().values("id", "name", "size")

#         # aggregate - запит до БД одразу, повертає один словник (мінімум, максимум, середнє, кількість)
#         # pizzas = PizzaModel.objects.aggregate(Min("price"), Max("price"), Avg("price"), Count("id"))

#         # values("name") + annotate - групування: скільки записів з кожною назвою
#         # pizzas = PizzaModel.objects.values("name").annotate(count=Count("name"))

#         # передаємо params з url у нашу функцію фільтрів, запиту до БД ще немає (QuerySet ледачий)
#         qs = filter_pizza(request.query_params)

#         # many=True - серіалізуємо список об'єктів, а не один. Запиту до БД ще немає
#         serializer = PizzaSerializer(instance=qs, many=True)

#         # serializer.data читає QuerySet - саме тут іде запит до БД
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:

#         # data - це дані від клієнта, instance не передано, тому save() викличе create()
#         serializer = PizzaSerializer(data=request.data)

#         # перевірка даних, якщо не пройшли - raise_exception кидає ValidationError, DRF повертає 400
#         serializer.is_valid(raise_exception=True)

#         # INSERT у БД: Django передає всі поля (created_at / updated_at він виставив сам), а БД повертає лише новий id, який Django записує в об'єкт у пам'яті (serializer.instance)
#         serializer.save()

#         # дані беруться з instance, повторного запиту до БД немає
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)


# class PizzaRetrieveUpdateDestroyView(APIView):

#     # допоміжний метод: знайти піцу за pk або повернути 404
#     def get_pizza(self, pk: int) -> PizzaModel:
#         try:
#             # objects.get() - метод ORM: шукає в БД один запис за pk і повертає готовий об'єкт
#             return PizzaModel.objects.get(pk=pk)
#         except PizzaModel.DoesNotExist:
#             # якщо запису немає, objects.get() кидає DoesNotExist - перекладаємо на NotFound, щоб клієнт отримав 404 з текстом, а не 500
#             raise NotFound(detail=f"Pizza with ID: {pk} not found")

#     def get(self, *args: Any, **kwargs: Any) -> Response:

#         # kwargs["pk"] - число з <int:pk> в urls.py
#         # запит до БД (SELECT) через get_pizza. 404, якщо піци немає
#         pizza = self.get_pizza(kwargs["pk"])

#         # об'єкт вже в пам'яті, нового запиту до БД немає
#         serializer = PizzaSerializer(pizza)
#         return Response(serializer.data, status.HTTP_200_OK)

#     def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:

#         # kwargs["pk"] - число з <int:pk> в urls.py
#         # запит до БД (SELECT) через get_pizza. 404, якщо піци немає
#         pizza = self.get_pizza(kwargs["pk"])

#         # передали instance (pizza) і data (request.data): тому save() викличе update(), а не create()
#         serializer = PizzaSerializer(pizza, request.data)

#         # перевірка даних, якщо не пройшли - raise_exception кидає ValidationError, DRF повертає 400
#         serializer.is_valid(raise_exception=True)

#         # save() викликає update(instance, validated_data): значення з validated_data записуються в об'єкт pizza в пам'яті (setattr), потім pizza.save() виконує UPDATE у БД
#         # updated_at при цьому оновлюється сам (auto_now), created_at не змінюється
#         serializer.save()

#         return Response(serializer.data, status.HTTP_200_OK)

#     def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         pizza = self.get_pizza(kwargs["pk"])

#         # partial=True: перевіряються лише передані поля, решта лишається як була (без нього відсутнє обов'язкове поле дало б 400)
#         serializer = PizzaSerializer(pizza, request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status.HTTP_200_OK)

#     def delete(self, *args: Any, **kwargs: Any) -> Response:

#         # знаходимо (404, якщо немає) і видаляємо запис з БД
#         self.get_pizza(kwargs["pk"]).delete()

#         # 204 No Content: успіх, тіло відповіді відсутнє
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # GenericAPIView дає інструменти (get_queryset, get_serializer, get_object), але сам нічого не виконує
# # дії дають міксини: ListModelMixin - list, CreateModelMixin - create
# # методи get і post пишемо самі й вручну передаємо в міксини.

# class PizzaListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):

#     # перевизначаємо get_queryset з GenericAPIView
#     # атрибут queryset з GenericAPIView лишається None, тут (в цьому класі) він не потрібен
#     def get_queryset(self):
#         return filter_pizza(self.request.query_params)

#     # який серіалізатор використовувати для цього view: GenericAPIView бере його в get_serializer()
#     # PizzaSerializer перевіряє дані від клієнта (POST) і перетворює об'єкти моделі на JSON у відповіді
#     serializer_class = PizzaSerializer

#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:

#         # шукаємо метод list серед батьківських класів (він у ListModelMixin)
#         # list бере записи через get_queryset(), серіалізує через get_serializer() і повертає Response
#         return super().list(request, *args, **kwargs)

#     def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:

#         # те саме з CreateModelMixin - create() використовує request.data для створення запису
#         return super().create(request, *args, **kwargs)

# те саме, що в PizzaListCreateView: GenericAPIView дає інструменти (get_queryset, get_serializer, get_object), а дії дають міксини: RetrieveModelMixin - retrieve, UpdateModelMixin - update і partial_update, DestroyModelMixin - destroy
# методи get, put, patch, delete пишемо самі й вручну передаємо в міксини.
# на відміну від списку, тут працюємо з одним записом: його знаходить get_object() за pk з url (<int:pk>)

# class PizzaRetrieveUpdateDestroyView(
#     GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
# ):
#     # get_queryset() у GenericAPIView бере його копію (.all()) на кожен запит, щоб не тягнути кеш попереднього звернення
#     queryset = PizzaModel.objects.all()

#     # який серіалізатор використовувати для цього view: GenericAPIView бере його в get_serializer()
#     # PizzaSerializer перевіряє дані від клієнта (PUT/PATCH) і перетворює об'єкти моделі на JSON у відповіді
#     serializer_class = PizzaSerializer

#     # кожен HTTP-метод передаємо у відповідний метод міксина (retrieve - один запис, update - PUT, partial_update - PATCH, destroy - DELETE)
#     # шукається об'єкт за pk через get_object() і самостійно повертається 404 та потрібні статуси (200, 204)
#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().retrieve(request, *args, **kwargs)

#     def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().update(request, *args, **kwargs)

#     def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().partial_update(request, *args, **kwargs)

#     def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().destroy(request, *args, **kwargs)


# ListCreateAPIView прив'язує HTTP-методи до міксинів: GET -> list (список), POST -> create (створення)
# ручний код з APIView вище (звернення до БД, серіалізатор, is_valid, save, Response) клас виконує сам: create перевіряє дані, зберігає й повертає 201 з даними створеної піци


class PizzaListCreateView(ListCreateAPIView):
    # який серіалізатор використовувати для цього view: GenericAPIView бере його в get_serializer()
    # POST: PizzaSerializer перевіряє дані від клієнта і викликає метод запису даних в БД
    # GET та POST: PizzaSerializer перетворює об'єкти моделі на JSON у відповіді
    serializer_class = PizzaSerializer

    # тут ми змінюємо стандартний query_set з GenericAPIView на власний
    def get_queryset(self):
        return filter_pizza(self.request.query_params)


# RetrieveUpdateDestroyAPIView вміє: GET -> retrieve, PUT -> update, PATCH -> partial_update, DELETE -> destroy
# Але в цьому класі PATCH свідомо заблокований через http_method_names: отримує 405 Method Not Allowed
# GET, PUT та DELETE шукають піцу за pk з url (get_object()) і якщо її немає, то повертають 404
# PUT вимагає всі обов'язкові поля (повна заміна)
# DELETE повертає 204 без тіла


class PizzaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    # з чого шукати об'єкт. get_queryset() бере його копію (.all()) на кожен запит, щоб не тягнути кеш попереднього
    queryset = PizzaModel.objects.all()

    # який серіалізатор використовувати для цього view: GenericAPIView бере його в get_serializer()
    # PUT: PizzaSerializer перевіряє тут дані від клієнта та викликає метод перезапису даних в БД
    # GET та PUT: PizzaSerializer перетворює об'єкти моделі на JSON у відповіді
    # DELETE серіалізатор не використовує: відповідь без тіла
    serializer_class = PizzaSerializer

    # дозволені HTTP-методи: GET, PUT, DELETE
    # PATCH клас підтримує, але він тут свідомо заблокований: отримує 405 Method Not Allowed
    http_method_names = ("get", "put", "delete")

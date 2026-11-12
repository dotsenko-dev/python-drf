# class PizzaListCreateView(APIView):
#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         # pizzas = (
#         #     PizzaModel.objects.filter(
#         #         (Q(size__gt=5) | Q(name="domino1")) & Q(price__gt=10)
#         #     ) # тут фільтр (по розміру більше >5 або ж по назві) та по ціні більше 10
#         #     .exclude(size=78) # тут виключити потім з попереднього фільтру розмір 78
#         #     .order_by("size", "-price") # знову ж таки від попереднього фільтру відсортувати по розміру і потім це все за спаданням ціни
#         #     .reverse() # і це все розвернути
#         # )
#         # pizzas = PizzaModel.objects.all()[1:6:2] # робимо запит до БД, де будемо брати лише з 1 по 5 індекс піци з кроком 2 (отримаємо піци з індексами 1, 3 та 5) (якби було [1:6], то запиту до БД ще не було б)
#         # pizzas = PizzaModel.objects.all().values("id", "name", "size") # тут замість об'єктів моделі в QuerySet повертаються словники з вказаними полями
#         # pizzas = PizzaModel.objects.aggregate(
#         #     Min("price"), Max("price"), Avg("price"), Count("id")
#         # ) # Тут одразу йде звернення до БД і повернення словника з мінімальною, максимальною, середньою ціною та кількість піц в БД
#         # pizzas = PizzaModel.objects.values("name").annotate(count=Count("name")) # annotate підраховує з БД, скільки разів є запис з цим значенням (тут це name) в БД і виводить його нам
#         # print(pizzas)
#         # pizzas = pizzas.filter((Q(size__gt=20) | Q(name="domino1")) & Q(price__gt=40)) # додаємо тут Q, щоб можна було не лише "так" робити фільтр, а і "або" додати. Якщо почали використовувати Q, то тепер в цій умові фільтрування лише його і треба скрізь тут використовувати
#         # qs = PizzaModel.objects.all()
#         qs = filter_pizza(request.query_params) # тут в нашу функцію filter_pizza передається з урли парамси (запиту до БД ще немає)
#         serializer = PizzaSerializer(instance=qs, many=True) # Ну і вже тут передається в наш серіалайзер (запиту до БД ще досі немає)
#         return Response(data=serializer.data, status=status.HTTP_200_OK) # а ось тут вже є запит до БД

#     def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         serializer = PizzaSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save() # тут робиться запис до БД і отримується назад лише id (модель попадає в instance)
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED) # тут вже не робиться повторно запит до БД, а робиться запит до instance


# class PizzaRetrieveUpdateDestroyView(APIView):
#     def get_pizza(self, pk: int) -> PizzaModel:
#         try:
#             return PizzaModel.objects.get(pk=pk) # Тут робиться запит до БД по pk і повертається вже готовий об'єкт піца
#         except PizzaModel.DoesNotExist:
#             raise NotFound(detail=f"Pizza with ID: {pk} not found")

#     def get(self, *args: Any, **kwargs: Any) -> Response:
#         pizza = self.get_pizza(kwargs["pk"])
#         serializer = PizzaSerializer(pizza) # тут вже не робиться запиту до БД, а береться наш об'єкт pizza
#         return Response(serializer.data, status.HTTP_200_OK) # запиту також до БД немає

#     def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         pizza = self.get_pizza(kwargs["pk"]) # запит до бд тут через get_pizza
#         serializer = PizzaSerializer(pizza, request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save() # ще один запит до бд
#         return Response(serializer.data, status.HTTP_200_OK)

#     def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         pizza = self.get_pizza(kwargs["pk"])
#         serializer = PizzaSerializer(pizza, request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status.HTTP_200_OK)

#     def delete(self, *args: Any, **kwargs: Any) -> Response:
#         self.get_pizza(kwargs["pk"]).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.pizza.filter import filter_pizza
from apps.pizza.models import PizzaModel
from apps.pizza.serializers import PizzaSerializer

# class PizzaListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
#     def get_queryset(self): # Тут ми перезаписуємо стандартний get_queryset в GenericAPIView на власний з фільтрами (queryset там залишається None, він нам тут не потрібен)
#         return filter_pizza(self.request.query_params)
#     serializer_class = PizzaSerializer # Тут так само в GenericAPIView перезаписуємо serializer_class з None на наш серіалізатор

#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         # Тут в наслідуваних модулях (super(), тут це GenericAPIView, ListModelMixin, CreateModelMixin) шукаємо метод list (він є в ListModelMixin) та передаємо в нього request (правда поки що не можу в'їхати, нащо?, ми ж його там не використовуємо), який в queryset записує викликаний метод get_queryset() і в serializer записує викликаний метод get_serializer() з GenericAPIView який в свою чергу використовує наш serializer_class (тобто PizzaSerializer)
#         return super().list(request, *args, **kwargs)

#     def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         # Тут для post те ж саме, але з CreateModelMixin і тут ми вже використовуємо для data наш request
#         return super().create(request, *args, **kwargs)


# class PizzaRetrieveUpdateDestroyView(
#     GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
# ):
#     # Тут в GenericAPIView в queryset замість None записуємо інструкцію-звернення до БД і там же, всередині GenericAPIView є метод get_queryset що робить при кожному запиті нову копію цієї інструкції (query.all()), щоб система не тягнула попередній кеш попереднього звернення
#     queryset = PizzaModel.objects.all()
#     serializer_class = PizzaSerializer

#     # Тут все те ж саме, що і вище ( звернення до відповідних міксинів)
#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().retrieve(request, *args, **kwargs)

#     def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().update(request, *args, **kwargs)

#     def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().partial_update(request, *args, **kwargs)

#     def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().destroy(request, *args, **kwargs)


# Тут все те ж саме, але ListCreateAPIView та RetrieveUpdateDestroyAPIView об'єднують в собі уже відповідні міксини
class PizzaListCreateView(ListCreateAPIView):
    serializer_class = PizzaSerializer

    def get_queryset(self):
        return filter_pizza(self.request.query_params)


class PizzaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PizzaModel.objects.all()
    serializer_class = PizzaSerializer
    # Тут треба прописати методи, які можливо опрацьовувати з postman
    http_method_names = ("get", "put", "delete")

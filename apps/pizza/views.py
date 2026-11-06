# from typing import Any

# from rest_framework import status
# from rest_framework.exceptions import NotFound
# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.pizza.filter import filter_pizza
# from apps.pizza.models import PizzaModel
# from apps.pizza.serializers import PizzaSerializer


# class PizzaListCreateView(APIView):
#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         # pizzas = (
#         #     PizzaModel.objects.filter(
#         #         (Q(size__gt=5) | Q(name="domino1")) & Q(price__gt=10)
#         #     )
#         #     .exclude(size=78)
#         #     .order_by("size", "-price")
#         #     .reverse()
#         # )
#         # pizzas = PizzaModel.objects.all()[1:6:2]
#         # pizzas = PizzaModel.objects.all().values("id", "name", "size")
#         # pizzas = PizzaModel.objects.aggregate(
#         #     Min("price"), Max("price"), Avg("price"), Count("id")
#         # )
#         # pizzas = PizzaModel.objects.values("name").annotate(count=Count("name"))
#         # print(pizzas)
#         # pizzas = pizzas.filter((Q(size__gt=20) | Q(name="domino1")) & Q(price__gt=40))
#         # qs = PizzaModel.objects.all()
#         qs = filter_pizza(request.query_params)
#         serializer = PizzaSerializer(instance=qs, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

#     def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         serializer = PizzaSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)


# class PizzaRetrieveUpdateDestroyView(APIView):
#     def get_pizza(self, pk: int) -> PizzaModel:
#         try:
#             return PizzaModel.objects.get(pk=pk)
#         except PizzaModel.DoesNotExist:
#             raise NotFound(detail=f"Pizza with ID: {pk} not found")

#     def get(self, *args: Any, **kwargs: Any) -> Response:
#         pizza = self.get_pizza(kwargs["pk"])
#         serializer = PizzaSerializer(pizza)
#         return Response(serializer.data, status.HTTP_200_OK)

#     def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         pizza = self.get_pizza(kwargs["pk"])
#         serializer = PizzaSerializer(pizza, request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
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
#     # queryset = PizzaModel.objects.all()
#     serializer_class = PizzaSerializer

#     def get_queryset(self):
#         return filter_pizza(self.request.query_params)

#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().list(request, *args, **kwargs)

#     def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().create(request, *args, **kwargs)


# class PizzaRetrieveUpdateDestroyView(
#     GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
# ):
#     queryset = PizzaModel.objects.all()
#     serializer_class = PizzaSerializer

#     def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().retrieve(request, *args, **kwargs)

#     def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().update(request, *args, **kwargs)

#     def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().partial_update(request, *args, **kwargs)

#     def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
#         return super().destroy(request, *args, **kwargs)


class PizzaListCreateView(ListCreateAPIView):
    serializer_class = PizzaSerializer

    def get_queryset(self):
        return filter_pizza(self.request.query_params)


class PizzaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PizzaModel.objects.all()
    serializer_class = PizzaSerializer
    # Якщо нам треба якийсь метод заборонити, то можна його не вказувати тут
    http_method_names = ("get", "put", "delete")

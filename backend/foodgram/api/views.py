from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import UsersApiPagination
from .permissions import OwnerOrAdminOrSafeMethods
from .serializers import (FavoritesSerializer, GetRecipeSerializer,
                          IngredientSerializer, RecipePostSerializer,
                          ShoppingCartSerializer, TagSerializer)
from recipes.models import (Favorites, Ingredient, Ingredients_Amount,
                            Recipe, ShoppingCart, Tag)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = (OwnerOrAdminOrSafeMethods,)
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)
    pagination_class = UsersApiPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return RecipePostSerializer

    @staticmethod
    def post_or_delete(request, model, serializer, pk):
        if request.method != 'POST':
            get_object_or_404(
                model,
                user=request.user,
                recipe=get_object_or_404(Recipe, id=pk)
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = serializer(
            data={'user': request.user.id, 'recipe': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return self.post_or_delete(
            request,
            Favorites,
            FavoritesSerializer,
            pk
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.post_or_delete(
            request,
            ShoppingCart,
            ShoppingCartSerializer,
            pk
        )

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = Ingredients_Amount.objects.filter(
            recipe__carts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('Handicraft', 'data/Handicraft.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('Handicraft', size=24)
        page.drawString(200, 800, 'Список покупок')
        page.setFont('Handicraft', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(75, height, (f'{i}. {name} - {data["amount"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import A4
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

    def canvas_method(self, ingredients):
        """
        Метод сохранения списка покупок в формате PDF.
        """
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment;filename = "shopping_cart.pdf'
        )
        begin_position_x, begin_position_y = 40, 650
        sheet = canvas.Canvas(response, pagesize=A4)
        pdfmetrics.registerFont(TTFont('FreeSans', 'data/FreeSans.ttf'))
        sheet.setFont('FreeSans', 50)
        sheet.setTitle('Список покупок')
        sheet.drawString(begin_position_x,
                         begin_position_y + 40, 'Список покупок: ')
        sheet.setFont('FreeSans', 24)
        for number, item in enumerate(ingredients, start=1):
            if begin_position_y < 100:
                begin_position_y = 700
                sheet.showPage()
                sheet.setFont('FreeSans', 24)
            sheet.drawString(
                begin_position_x,
                begin_position_y,
                f'{number}.  {item["ingredient__name"]} - '
                f'{item["ingredient_total"]}'
                f' {item["ingredient__measurement_unit"]}'
            )
            begin_position_y -= 30
        sheet.showPage()
        sheet.save()
        return response

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, pk=None):
        """
        Метод создания списка покупок.
        """
        ingredients = Ingredients_Amount.objects.filter(
            recipe__shopping_cart__user=request.user.id
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(ingredient_total=Sum('amount'))
        return self.canvas_method(ingredients)

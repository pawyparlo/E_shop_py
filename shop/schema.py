import graphene
from graphene_django import DjangoObjectType
from shop.models.categories import Category
from shop.models.products import Product


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "slug",
            "image",
            "description",
            "price",
            "available",
            "created",
            "updated",
        )


class Query(graphene.ObjectType):
    product = graphene.Field(ProductType, product_id=graphene.ID(required=True))
    products = graphene.List(ProductType)
    products_by_category = graphene.List(
        ProductType, category_name=graphene.String(required=True)
    )

    @staticmethod
    def resolve_products(_root, _info):
        return Product.objects.all()

    @staticmethod
    def resolve_product(_root, _info, product_id):
        return Product.objects.get(pk=product_id)

    @staticmethod
    def resolve_products_by_category(_root, _info, category_name):
        return Product.objects.filter(category__name=category_name)


schema = graphene.Schema(query=Query)
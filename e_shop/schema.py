import graphene

# import e_shop.shop.schema as shop
from shop.schema import ProductsQuery


class Query(ProductsQuery):
    pass


# class Mutation(shop.Mutation):
#     pass


schema = graphene.Schema(query=ProductsQuery)

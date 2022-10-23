import graphene

# import e_shop.shop.schema as shop
from shop.schema import ProductsQuery
from orders.schema import QueryOrder, CreateOrder


class Query(ProductsQuery, QueryOrder):
    pass


class Mutation(CreateOrder):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

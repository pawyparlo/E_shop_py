import graphene

# import e_shop.shop.schema as shop
from shop.schema import Query


class Query(Query):
    pass


# class Mutation(shop.Mutation):
#     pass


schema = graphene.Schema(query=Query)

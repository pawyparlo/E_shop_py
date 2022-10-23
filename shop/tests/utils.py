import json
import random
from unicodedata import category
import uuid
from graphql import GraphQLError
from shop.models.products import Product
from shop.models.categories import Category


class QueryRunner:
    @staticmethod
    def run(cursor, query, **kwargs):
        response = cursor.query(query, **kwargs)
        if "errors" in json.loads(response.content):
            raise GraphQLError(json.loads(response.content)["errors"][0]["message"])
        return json.loads(response.content)


class Generate:
    _id = 0

    @staticmethod
    def category(**kwargs):
        name = Generate.name_field(main_part="Generic category")
        if "name" not in kwargs:
            kwargs["name"] = name
        if "slug" not in kwargs:
            kwargs["slug"] = name.lower().replace(" ", "")
        category = Category.objects.create(**kwargs)
        return category

    @staticmethod
    def product(**kwargs):
        if "category" not in kwargs:
            kwargs["category"] = Generate.category()
        if "name" not in kwargs:
            kwargs["name"] = Generate.name_field(main_part="Generic product")
        if "description" not in kwargs:
            kwargs["description"] = "Description example vol {}".format(Generate._id)
        if "price" not in kwargs:
            kwargs["price"] = Generate.price_field()
        product = Product.objects.create(**kwargs)
        return product

    @staticmethod
    def _id_field():
        Generate._id = +1
        return Generate._id

    @staticmethod
    def name_field(main_part="Generic"):
        return "".join([main_part, str(uuid.uuid4())])

    @staticmethod
    def price_field():
        return random.randint(10, 100)

import json
import random
from unicodedata import category
import uuid
from typing import List, Dict
from graphql import GraphQLError
from shop.models.products import Product
from shop.models.categories import Category
from orders.models import Order, OrderItem


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
        if "name" not in kwargs:
            name = Generate.name_field(main_part="Generic category")
            kwargs["name"] = name
            kwargs["slug"] = name.lower().replace(" ", "")

        kwargs["slug"] = kwargs["name"].lower().replace(" ", "")
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
    def order(**kwargs):
        if "first_name" not in kwargs:
            kwargs["first_name"] = Generate.human_first_name_field()
        if "last_name" not in kwargs:
            kwargs["last_name"] = Generate.human_last_name_field()
        if "email" not in kwargs:
            kwargs["email"] = Generate.email(
                first_name=kwargs["first_name"], last_name=kwargs["last_name"]
            )
        if "address" not in kwargs:
            kwargs["address"] = Generate.address()
        if "city" not in kwargs:
            kwargs["city"] = Generate.city()

        order = Order.objects.create(**kwargs)

        if "items" not in kwargs:
            products = [Generate.product() for _ in range(0, 5)]
            ordered_items = [
                OrderItem.objects.create(
                    product=product, order=order, quantity=random.randint(0, 10)
                )
                for product in products
            ]

        return order

    @staticmethod
    def _id_field():
        Generate._id = +1
        return Generate._id

    @staticmethod
    def name_field(main_part="Generic"):
        return "".join([main_part, str(uuid.uuid4())])

    @staticmethod
    def human_first_name_field(name=None):
        choices = ["Angie", "Joe", "Bradd", "Stanley"]
        if name:
            return name
        return choices[random.randint(0, len(choices) - 1)]

    @staticmethod
    def human_last_name_field(name=None):
        choices = ["Kubrick", "Monroe", "Wesley", "Potter"]
        if name:
            return name
        return choices[random.randint(0, len(choices) - 1)]

    @staticmethod
    def email(first_name, last_name):
        return f"{first_name}.{last_name}@test.com"

    @staticmethod
    def address(address=None):
        streets = ["avenue", "East side street", "West side street", "avenue"]
        if address:
            return address
        return f"{random.randint(1,30)} {streets[random.randint(0, len(streets) - 1)]}"

    @staticmethod
    def city(name=None):
        choices = ["Seattle", "New York", "Chicago", "New Yersey"]
        if name:
            return name
        return choices[random.randint(0, len(choices) - 1)]

    @staticmethod
    def price_field():
        return random.randint(10, 100)


class Assert:
    @staticmethod
    def has_params(dictionary: dict, params_name: List[str]):
        warnings = []
        for param_name in params_name:
            try:
                dictionary[param_name]
            except Exception:
                warnings.append(KeyError(f"Param '{param_name}' not found"))
        if warnings:
            raise BaseException(warnings)


class UtilsHelpers:
    @staticmethod
    def next_missing_field(fields: List[str], input: Dict[str, str]):
        for field_name in fields:
            try:
                input[field_name]
            except:
                return field_name

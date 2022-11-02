from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from shop.tests.utils import QueryRunner, Generate, Assert
from orders.models import Order
import json


class OrderQueries:
    class Fields:
        ORDER_FIELDS = """
            firstName
            lastName
            email
            address
            city
            paid
            items {
            quantity
            product {
                id
                name
                category {
                name
                }
                price
                available
                }
            }
        """

    @staticmethod
    def get_order(cursor, **kwargs):
        return QueryRunner.run(cursor, OrderQueries.GET_ORDER, **kwargs)["data"][
            "order"
        ]

    GET_ORDER = f"""
        query getOrder($orderId: ID!) {{
            order(orderId: $orderId) {{
                firstName
                lastName
                email
                address
                city
                paid
                items {{
                quantity
                product {{
                    id
                    name
                    category {{
                    name
                    }}
                    price
                    available
                    }}
                }}
            }}
        }}
    """

    @staticmethod
    def get_orders(cursor, **kwargs):
        return QueryRunner.run(cursor, OrderQueries.GET_ORDERS, **kwargs)["data"][
            "orders"
        ]

    GET_ORDERS = f"""
        query getOrders {{
            orders {{
                firstName
                lastName
                email
                address
                city
                paid
                items {{
                quantity
                product {{
                    id
                    name
                    category {{
                    name
                    }}
                    price
                    available
                    }}
                }}
            }}
        }}
    """

    @staticmethod
    def create_order(cursor, **kwargs):
        return QueryRunner.run(cursor, OrderQueries.CREATE_ORDER, **kwargs)

    CREATE_ORDER = f"""
        mutation createOrder($input: OrderCreateInput!) {{
        createOrder(orderInput: $input) {{
            completed
            }}
        }}
    """


class QueryOrderTestCase(GraphQLTestCase):
    def setUp(self):
        self.category_1 = Generate.category(name="fruits")
        self.product_1 = Generate.product(
            category=self.category_1, name="Banana", price=100.5, available=True
        )
        self.product_2 = Generate.product(
            category=self.category_1, name="Apple", price=55.5, available=True
        )
        self.product_3 = Generate.product(
            category=self.category_1, name="Orange", price=25.1, available=True
        )

    def test_query_orders(self):
        order_1 = Generate.order()
        order_2 = Generate.order()
        order_3 = Generate.order()

        orders = OrderQueries.get_orders(self)

        Assert.has_params(
            orders[0],
            ["firstName", "lastName", "email", "address", "city", "items"],
        )
        Assert.has_params(
            orders[1],
            ["firstName", "lastName", "email", "address", "city", "items"],
        )
        Assert.has_params(
            orders[2],
            ["firstName", "lastName", "email", "address", "city", "items"],
        )

        self.assertEqual(len(orders), 3)
        self.assertEqual(len(Order.objects.all()), 3)
        self.assertEqual(len(orders[0]["items"]), 5)
        self.assertEqual(len(orders[1]["items"]), 5)
        self.assertEqual(len(orders[2]["items"]), 5)

    def test_query_order(self):
        order_1 = Generate.order()

        order = OrderQueries.get_order(self, variables={"orderId": 1})

        Assert.has_params(
            order,
            ["firstName", "lastName", "email", "address", "city", "items"],
        )

        self.assertEqual(len(order["items"]), 5)
        self.assertEqual(len(Order.objects.all()), 1)


class CreateOrderTestCase(GraphQLTestCase):
    pass
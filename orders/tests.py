from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from shop.tests.utils import QueryRunner, Generate


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
        return QueryRunner.run(cursor, OrderQueries.GET_ORDER, **kwargs)

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
        return QueryRunner.run(cursor, OrderQueries.GET_ORDERS, **kwargs)

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

    def test_test(self):
        order = Generate.order()
        print(order.first_name)
        print(order.last_name)
        print(order.email)
        print(order.address)
        print(order.city)

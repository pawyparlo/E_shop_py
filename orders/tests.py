from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from shop.tests.utils import QueryRunner, Generate, Assert, UtilsHelpers
from orders.models import Order, OrderItem
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
        return QueryRunner.run(cursor, OrderQueries.CREATE_ORDER, **kwargs)["data"][
            "createOrder"
        ]

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

    def test_query_orders_have_proper_item_fields(self):
        order_1 = Generate.order()

        orders = OrderQueries.get_orders(self)

        self.assertEqual(len(orders[0]["items"]), 5)

        Assert.has_params(
            orders[0]["items"][0],
            ["quantity", "product"],
        )
        Assert.has_params(
            orders[0]["items"][0]["product"],
            ["id", "name", "category", "available"],
        )

    def test_query_order(self):
        order_1 = Generate.order()

        order = OrderQueries.get_order(self, variables={"orderId": 1})

        Assert.has_params(
            order,
            ["firstName", "lastName", "email", "address", "city", "items"],
        )

        self.assertEqual(len(order["items"]), 5)
        self.assertEqual(len(Order.objects.all()), 1)

    def test_query_order_has_proper_item_fields(self):
        order_1 = Generate.order()

        order = OrderQueries.get_order(self, variables={"orderId": 1})

        Assert.has_params(
            order["items"][0],
            ["quantity", "product"],
        )
        Assert.has_params(
            order["items"][0]["product"],
            ["id", "name", "category", "available"],
        )
        self.assertEqual(OrderItem.objects.count(), 5)


class CreateOrderTestCase(GraphQLTestCase):
    _required_fields_names = [
        "firstName",
        "lastName",
        "email",
        "address",
        "city",
    ]

    def test_create_order_without_items(self):
        order_input = {
            "firstName": "Billy",
            "lastName": "Parrot",
            "email": "billy@billy.com",
            "address": "Avenue 3",
            "city": "New York",
        }

        order = OrderQueries.create_order(
            self,
            variables={"input": order_input},
        )

        order_from_db = Order.objects.first()

        self.assertIn("completed", order)
        self.assertEqual(order["completed"], True)
        self.assertEqual(Order.objects.count(), 1)

        self.assertEqual(order_from_db.id, 1)
        self.assertEqual(order_from_db.first_name, order_input["firstName"])
        self.assertEqual(order_from_db.last_name, order_input["lastName"])
        self.assertEqual(order_from_db.email, order_input["email"])
        self.assertEqual(order_from_db.address, order_input["address"])
        self.assertEqual(order_from_db.city, order_input["city"])

    def test_create_order_with_missing_last_name_fail(self):
        order_input = {
            "firstName": "Billy",
            "email": "billy@billy.com",
            "address": "Avenue 3",
            "city": "New York",
        }

        next_missing_field = UtilsHelpers.next_missing_field(
            fields=self._required_fields_names, input=order_input
        )
        with self.assertRaisesMessage(
            Exception,
            f"$input' got invalid value {order_input}; Field '{next_missing_field}' of required type 'String!' was not provided.",
        ):
            OrderQueries.create_order(
                self,
                variables={"input": order_input},
            )

        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_missing_email_fail(self):
        order_input = {
            "firstName": "Billy",
            "lastName": "Parrot",
            "address": "Avenue 3",
            "city": "New York",
        }

        next_missing_field = UtilsHelpers.next_missing_field(
            fields=self._required_fields_names, input=order_input
        )
        with self.assertRaisesMessage(
            Exception,
            f"$input' got invalid value {order_input}; Field '{next_missing_field}' of required type 'String!' was not provided.",
        ):
            OrderQueries.create_order(
                self,
                variables={"input": order_input},
            )

        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_missing_address_fail(self):
        order_input = {
            "firstName": "Billy",
            "lastName": "Parrot",
            "email": "billy@billy.com",
            "city": "New York",
        }

        next_missing_field = UtilsHelpers.next_missing_field(
            fields=self._required_fields_names, input=order_input
        )
        with self.assertRaisesMessage(
            Exception,
            f"$input' got invalid value {order_input}; Field '{next_missing_field}' of required type 'String!' was not provided.",
        ):
            OrderQueries.create_order(
                self,
                variables={"input": order_input},
            )

        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_missing_city_fail(self):
        order_input = {
            "firstName": "Billy",
            "lastName": "Parrot",
            "email": "billy@billy.com",
            "address": "Avenue 3",
        }

        next_missing_field = UtilsHelpers.next_missing_field(
            fields=self._required_fields_names, input=order_input
        )
        with self.assertRaisesMessage(
            Exception,
            f"$input' got invalid value {order_input}; Field '{next_missing_field}' of required type 'String!' was not provided.",
        ):
            OrderQueries.create_order(
                self,
                variables={"input": order_input},
            )

        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_with_single_item(self):
        product_1 = Generate.product(
            category=Generate.category(name="Fruits"),
            name="banana",
            description="This is banana",
            price=100,
        )
        item_input = [{"productId": 1, "quantity": 10}]

        order_input = {
            "firstName": Generate.human_first_name_field(),
            "lastName": Generate.human_last_name_field(),
            "email": Generate.email(first_name="test", last_name="email"),
            "address": Generate.address(),
            "city": Generate.city(),
            "orderedItems": item_input,
        }

        order = OrderQueries.create_order(
            self,
            variables={"input": order_input},
        )

        order_from_db = Order.objects.first()
        ordered_items_from_db = OrderItem.objects.filter(order=order_from_db)

        self.assertIn("completed", order)
        self.assertEqual(order["completed"], True)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(len(ordered_items_from_db), 1)
        self.assertEqual(ordered_items_from_db[0].id, 1)
        self.assertEqual(ordered_items_from_db[0].quantity, 10)
        self.assertEqual(ordered_items_from_db[0].product.name, "banana")
        self.assertEqual(ordered_items_from_db[0].product.description, "This is banana")
        self.assertEqual(ordered_items_from_db[0].product.price, 100)
        self.assertEqual(ordered_items_from_db[0].product.category.name, "Fruits")

    def test_create_order_with_multiple_items(self):
        product_1 = Generate.product()
        product_2 = Generate.product()
        product_3 = Generate.product()

        item_input = [
            {"productId": 1, "quantity": 10},
            {"productId": 2, "quantity": 5},
            {"productId": 3, "quantity": 15},
            ]

        order_input = {
            "firstName": Generate.human_first_name_field(),
            "lastName": Generate.human_last_name_field(),
            "email": Generate.email(first_name="test", last_name="email"),
            "address": Generate.address(),
            "city": Generate.city(),
            "orderedItems": item_input,
        }

        order = OrderQueries.create_order(
            self,
            variables={"input": order_input},
        )

        order_from_db = Order.objects.first()
        ordered_items_from_db = OrderItem.objects.filter(order=order_from_db)

        self.assertIn("completed", order)
        self.assertEqual(order["completed"], True)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(len(ordered_items_from_db), 3)
        self.assertEqual(ordered_items_from_db[0].id, 1)
        self.assertEqual(ordered_items_from_db[1].id, 2)
        self.assertEqual(ordered_items_from_db[2].id, 3)
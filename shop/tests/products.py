from graphene_django.utils.testing import GraphQLTestCase
from .utils import QueryRunner, Generate


class ProductQueries:
    class Fields:
        PRODUCT_FIELDS = """
            id,
            category {
                name
            }
            name,
            slug,
            image,
            description,
            price,
            available,
            created,
            updated
        """

    @staticmethod
    def get_product(cursor, **kwargs):
        return QueryRunner.run(cursor, ProductQueries.GET_PRODUCT, **kwargs)["data"][
            "product"
        ]

    GET_PRODUCT = f"""
        query getProduct($productId: ID!) {{
            product(productId: $productId) {{
                {Fields.PRODUCT_FIELDS}
            }}
        }}
    """

    @staticmethod
    def get_products(cursor, **kwargs):
        return QueryRunner.run(cursor, ProductQueries.GET_PRODUCTS, **kwargs)["data"][
            "products"
        ]

    GET_PRODUCTS = f"""
        query getProducts {{
            products {{
                {Fields.PRODUCT_FIELDS}
            }}
        }}
    """


class QueryProductsTestCase(GraphQLTestCase):
    def setUp(self):
        self.category_1 = Generate.category(name="fruits")
        self.product_1 = Generate.product(
            category=self.category_1,
            name="banana",
            description="This is banana",
            price=100.50,
            available=True,
        )
        self.product_2 = Generate.product()
        self.product_3 = Generate.product()

    def test_get_products(self):
        products = ProductQueries.get_products(self)

        self.assertEqual(len(products), 3)

    def test_get_product(self):
        product = ProductQueries.get_product(self, variables={"productId": 1})

        self.assertEqual(product["name"], self.product_1.name)
        self.assertEqual(product["category"]["name"], self.product_1.category.name)
        self.assertEqual(product["description"], self.product_1.description)
        self.assertEqual(float(product["price"]), self.product_1.price)
        self.assertEqual(product["available"], self.product_1.available)
        
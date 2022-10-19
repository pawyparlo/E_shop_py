from django.test import TestCase
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
        return QueryRunner.run(cursor, ProductQueries.GET_PRODUCT, **kwargs)["data"]

    GET_PRODUCT = f"""
        query getProduct($productId: ID!) {{
            product(productId: $productId) {{
                {Fields.PRODUCT_FIELDS}
            }}
        }}
    """

    @staticmethod
    def get_products(cursor, **kwargs):
        return QueryRunner.run(cursor, ProductQueries.GET_PRODUCTS, **kwargs)

    GET_PRODUCTS = f"""
        query getProducts {{
            products {{
                {Fields.PRODUCT_FIELDS}
            }}
        }}
    """


class QueryProductsTestCase(GraphQLTestCase):
    def setUp(self):
        self.product_1 = Generate.product()
        # self.product_2 = Generate.product()
        # self.product_3 = Generate.product()

    def test_get_products(self):
        response = ProductQueries.get_products(self)
        print(response)
        # self.assertEqual(4, le)

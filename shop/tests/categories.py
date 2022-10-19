from django.test import TestCase
from .utils import QueryRunner, Generate


class QueriesTest(TestCase):
    class Fields:
        CATEGORY_FIELDS = """
            id,
            name,
            slug
        """

    GET_CATEGORIES = f"""
        query getCategories {{
            categories {{
                {Fields.CATEGORY_FIELDS}
            }}
        }}
    """

    def test_resolve_products_query(self):
        pass

    def test_second_test(self):
        pass

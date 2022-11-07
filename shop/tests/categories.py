from .utils import QueryRunner, Generate
from graphene_django.utils.testing import GraphQLTestCase


class CategoriesQueries:
    class Fields:
        CATEGORY_FIELDS = """
            id,
            name,
            image,
            slug
        """

    GET_CATEGORIES = f"""
        query getCategories {{
            categories {{
                {Fields.CATEGORY_FIELDS}
            }}
        }}
    """

    def get_category(cursor, **kwargs):
        return QueryRunner.run(cursor, CategoriesQueries.GET_CATEGORIES, **kwargs)[
            "data"
        ]["categories"]


class QueryCategoriesTestCase(GraphQLTestCase):
    def setUp(self):
        self.category_1 = Generate.category()
        self.category_2 = Generate.category()
        self.category_3 = Generate.category()

    def test_query_all_categories(self):
        categories = CategoriesQueries.get_category(self)

        self.assertEqual(len(categories), 3)

        result_categories_names = [category["name"] for category in categories]

        self.assertTrue(self.category_1.name in result_categories_names)
        self.assertTrue(self.category_2.name in result_categories_names)
        self.assertTrue(self.category_3.name in result_categories_names)

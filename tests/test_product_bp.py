
import unittest
from app import application as app

class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list_page(self):
        """Тест маршруту /products/."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        # Перевіримо, чи є на сторінці назва одного з наших товарів
        self.assertIn(b"Alpha", response.data)
        self.assertIn(b"Omega", response.data)

    def test_product_details_page(self):
        """Тест маршруту /products/<id>."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        # Перевіримо, чи сторінка повернула ID товару
        self.assertIn(b"ID: 1", response.data)

        response_2 = self.client.get("/products/2")
        self.assertEqual(response_2.status_code, 200)
        self.assertIn(b"ID: 2", response_2.data)

if __name__ == "__main__":
    unittest.main()
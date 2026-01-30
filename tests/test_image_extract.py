import unittest
from extract_image import get_images_from_html


class TestImageExtraction(unittest.TestCase):
    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="https://blog.boot.dev/logo.png" alt="Image"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self):
        input_url = "https://blog.boot.dev"
        input_body = """
        <html>
            <body>
                <img src="/image1.png" alt="Image 1">
                <img src="https://blog.boot.dev/image2.png" alt="Image 2">
                <img src="/image3.jpg" alt="Image 3">
            </body>
        </html>
        """
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://blog.boot.dev/image1.png",
            "https://blog.boot.dev/image2.png",
            "https://blog.boot.dev/image3.jpg",
        ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        input_url = "https://blog.boot.dev"
        input_body = "<html><body><p>No images here!</p></body></html>"
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img alt="no src here"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

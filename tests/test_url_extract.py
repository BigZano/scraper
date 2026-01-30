import unittest
from extract_url import get_urls_from_html


class TestUrlExtract(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_all(self):
        input_url = "https://blog.boot.dev"
        input_body = """
        <html>
            <body>
                <a href="https://blog.boot.dev"><span>Boot.dev</span></a>
                <a href="/courses"><span>Courses</span></a>
                <a href="https://blog.boot.dev/courses/python"><span>Python Course</span></a>
            </body>
        </html>
        """
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://blog.boot.dev",
            "https://blog.boot.dev/courses",
            "https://blog.boot.dev/courses/python",
        ]
        self.assertCountEqual(actual, expected)

    def test_get_urls_from_html_none(self):
        input_url = "https://blog.boot.dev"
        input_body = "<html><body><span>No links here!</span></body></html>"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

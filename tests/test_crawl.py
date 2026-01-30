import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_caps(self):
        input_url = "HTTPS://BLOG.BOOT.DEV/PATH"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_trailing_slash(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    # def test_normalize_query(self):
    #   input_url = "https://blog.boot.dev/path?query=3&query=4&query=2&query=1"
    #   actual = normalize_url(input_url)
    #   expected = "blog.boot.dev/path?query=1&query=2&query=3&query=4"
    #   self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

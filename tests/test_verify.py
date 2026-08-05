import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import verify  # noqa: E402


class TestLinkParsing(unittest.TestCase):
    def _urls(self, text: str) -> list[str]:
        return list(verify.iter_urls(text))

    def test_trailing_punctuation_stripped(self):
        self.assertEqual(self._urls("see https://a.com/x, and"), ["https://a.com/x"])

    def test_trailing_paren_unbalanced(self):
        self.assertEqual(self._urls("(https://a.com/x)"), ["https://a.com/x"])

    def test_balanced_paren_kept(self):
        self.assertEqual(self._urls("https://a.com/x(y)"), ["https://a.com/x(y)"])

    def test_semicolon_does_not_merge(self):
        self.assertEqual(
            self._urls("https://a.com/a;https://b.com/b"),
            ["https://a.com/a", "https://b.com/b"],
        )

    def test_backtick_code_span_excluded(self):
        self.assertEqual(self._urls("run `http://127.0.0.1:8121/x`"), [])

    def test_angle_brackets_excluded(self):
        self.assertEqual(self._urls("<https://a.com/x>"), ["https://a.com/x"])

    def test_dev_host_skipped_in_cmd(self):
        urls: dict[str, str] = {}
        for url in verify.iter_urls("[x](http://localhost:8000/)"):
            host = __import__("urllib.parse", fromlist=["urlsplit"]).urlsplit(url).hostname or ""
            if host in verify._DEV_HOSTS or host.endswith(".localhost"):
                continue
            urls[url] = "t"
        self.assertEqual(urls, {})


class TestCleanUrl(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(verify.clean_url("https://a.com/x"), "https://a.com/x")

    def test_periods(self):
        self.assertEqual(verify.clean_url("https://a.com/x."), "https://a.com/x")


if __name__ == "__main__":
    unittest.main()

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from pull import anthropic, hn, lobsters, strip_tags


def fixture(name):
    with open(os.path.join(HERE, "fixtures", name)) as f:
        return f.read()


class TestParsers(unittest.TestCase):
    def test_hn_returns_title_score_pairs(self):
        items = hn(fixture("hackernews.html"))
        self.assertTrue(items)
        for title, score in items:
            self.assertIsInstance(title, str)
            self.assertIsInstance(score, int)

    def test_hn_contains_real_story(self):
        titles = [t for t, _ in hn(fixture("hackernews.html"))]
        self.assertIn("Don't be a meat proxy", titles)

    def test_lobsters_contains_real_story(self):
        titles = lobsters(fixture("lobsters.html"))
        self.assertIn("Don't be a meat proxy", titles)

    def test_anthropic_cards(self):
        cards = anthropic(fixture("anthropic.html"))
        self.assertTrue(any("Claude Opus 5" in c for c in cards))
        self.assertTrue(any("open-weights" in c for c in cards))

    def test_strip_tags_handles_entities(self):
        self.assertEqual(strip_tags("<b>Don&#39;t &amp; co</b>"), "Don't & co")


if __name__ == "__main__":
    unittest.main()

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from pull import anthropic, collect, hn, lobsters, strip_tags, write_digest


def fixture(name):
    with open(os.path.join(HERE, "fixtures", name)) as f:
        return f.read()


class TestParsers(unittest.TestCase):
    def test_hn_returns_title_url_score(self):
        items = hn(fixture("hackernews.html"))
        self.assertTrue(items)
        for title, url, score in items:
            self.assertIsInstance(title, str)
            self.assertTrue(url.startswith("http"))
            self.assertIsInstance(score, int)

    def test_hn_contains_real_story(self):
        titles = [t for t, _, _ in hn(fixture("hackernews.html"))]
        self.assertIn("Don't be a meat proxy", titles)

    def test_hn_urls_are_external(self):
        urls = [u for _, u, _ in hn(fixture("hackernews.html"))]
        self.assertTrue(all(u.startswith("http") for u in urls))

    def test_lobsters_contains_real_story(self):
        titles = [t for t, _, _ in lobsters(fixture("lobsters.html"))]
        self.assertIn("Don't be a meat proxy", titles)

    def test_lobsters_urls(self):
        urls = [u for _, u, _ in lobsters(fixture("lobsters.html"))]
        self.assertTrue(any("gruhn.me" in u for u in urls))

    def test_anthropic_cards(self):
        cards = anthropic(fixture("anthropic.html"))
        self.assertTrue(any("Claude Opus 5" in c for c, _, _ in cards))
        self.assertTrue(any("open-weights" in c for c, _, _ in cards))

    def test_anthropic_urls_are_absolute(self):
        urls = [u for _, u, _ in anthropic(fixture("anthropic.html"))]
        self.assertTrue(any(u == "https://www.anthropic.com/news/claude-opus-5" for u in urls))

    def test_strip_tags_handles_entities(self):
        self.assertEqual(strip_tags("<b>Don&#39;t &amp; co</b>"), "Don't & co")


class TestDigest(unittest.TestCase):
    DATA = {
        "Hacker News (front page)": [
            ("Story A", "https://a.example/1", 42),
            ("Story B", "https://b.example/2", 0),
        ],
        "Lobsters": [
            ("Story C", "https://c.example/3", 0),
            ("Story C", "https://c.example/3", 0),  # duplicate URL must collapse
        ],
        "Anthropic (anthropic.com/news)": [
            ("Story D", "https://www.anthropic.com/news/foo", 0),
        ],
        "failed": [],
    }

    def test_digest_note_shape(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            import pull

            old = pull.os.path.dirname
            pull.os.path.dirname = lambda p: tmp
            try:
                out = write_digest(self.DATA, summarize=lambda t, m: "## Summary\n- ok")
            finally:
                pull.os.path.dirname = old
            with open(out) as f:
                text = f.read()
            self.assertIn("Provenance: AI-drafted (nano local model, headlines only)", text)
            self.assertIn("## Summary", text)
            self.assertIn("- ok", text)
            self.assertIn("## Further reading", text)
            self.assertEqual(text.count("https://c.example/3"), 1, "duplicate URL collapsed")
            self.assertIn("Story A — https://a.example/1", text)

    def test_digest_raw_fallback_when_ollama_down(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            import pull

            old = pull.os.path.dirname
            pull.os.path.dirname = lambda p: tmp
            try:
                out = write_digest(
                    self.DATA, summarize=lambda t, m: "## Summary\n- summarizer unavailable: no ollama"
                )
            finally:
                pull.os.path.dirname = old
            with open(out) as f:
                text = f.read()
            self.assertIn("Ollama not reachable", text)
            self.assertIn("Story A", text)


if __name__ == "__main__":
    unittest.main()

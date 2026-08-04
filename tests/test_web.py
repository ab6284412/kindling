import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from web import render, state  # noqa: E402

DRILL_FIXTURE = """# Drill: read Authentication-Results
Source: `knowledge/dmarc-caveat.md`
Provenance: AI-drafted · Credits: SenderLedger (publication)

Goal: judge whether "passed DMARC" means anything in a given message.

Steps:
1. Send yourself an email.
2. Read the `Authentication-Results:` header.
3. Answer: did it pass SPF, DKIM, DMARC?

Self-check (pass/fail): you can explain what `p=`, `sp=`, `rua`, and "alignment" mean.

Why this matters: mail pipelines treat passing DMARC as trust.
"""


class TestState(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.original = state.STATE_PATH
        state.STATE_PATH = self.tmp.name

    def tearDown(self):
        state.STATE_PATH = self.original
        os.unlink(self.tmp.name)

    def test_roundtrip(self):
        s = state.load()
        self.assertTrue(state.toggle(s, "drill", "drills/x.md"))
        self.assertTrue(state.toggle(s, "stage", "FastAPI"))
        self.assertEqual(s["drills"], {"drills/x.md": True})
        self.assertEqual(s["stages"], {"FastAPI": True})
        state.save(s)
        self.assertEqual(state.load(), s)

    def test_corrupt_file_falls_back_to_default(self):
        with open(self.tmp.name, "w") as f:
            f.write("{not json")
        self.assertEqual(state.load(), state.default_state())

    def test_missing_file_is_default(self):
        state.STATE_PATH = os.path.join(self.tmp.name, "nope.json")
        self.assertEqual(state.load(), state.default_state())

    def test_blank_note_deletes(self):
        s = state.load()
        state.set_note(s, "drills/x.md", "remember this")
        self.assertEqual(s["notes"]["drills/x.md"], ["remember this"])
        state.set_note(s, "drills/x.md", "   ")
        self.assertNotIn("drills/x.md", s["notes"])


class TestPathSafety(unittest.TestCase):
    def test_ok(self):
        self.assertTrue(render.resolve_content_path("concepts/http-request-response.md"))
        self.assertTrue(render.resolve_content_path("learning.md"))

    def test_traversal_rejected(self):
        for bad in (
            "../etc/passwd",
            "concepts/../../learning.md",
            "..",
            "/etc/passwd",
            "drills/..%2f..",
            "concepts/x.txt",
            "misc/foo.md",
        ):
            self.assertIsNone(render.resolve_content_path(bad))

    def test_new_pillars_resolvable(self):
        for p in ("dsa/hashing.md", "soft-skills/rubber-duck-debugging.md",
                  "soft-skills/communication-skills/jargon/idempotency.md",
                  "dsa/puzzles/bridge-and-torch.md"):
            self.assertTrue(render.resolve_content_path(p))

    def test_dsa_roadmap_order(self):
        items = render.list_content("dsa")
        self.assertIsNotNone(items)
        names = [i.split("/")[-1] for i in items]
        self.assertEqual(names[0], "big-o-notation.md")
        self.assertEqual(names.index("two-pointers.md") > names.index("arrays-strings.md"), True)


class TestParse(unittest.TestCase):
    def test_drill(self):
        d = render.parse_drill(DRILL_FIXTURE)
        self.assertEqual(d["title"], "Drill: read Authentication-Results")
        self.assertIn("judge whether", d["goal"])
        self.assertIn("Send yourself an email", d["steps"])
        self.assertIn("alignment", d["self_check"])

    def test_learning_stages(self):
        with open(os.path.join(render.ROOT, "learning.md"), encoding="utf-8") as f:
            stages = render.parse_stages(f.read())
        self.assertEqual(len(stages), 7)
        self.assertIn("Language foundation: Python + tooling — from zero", stages)
        self.assertIn("The request/response core", stages)


class TestLinkify(unittest.TestCase):
    def test_bare_url_becomes_link(self):
        html = render.render_markdown("- see https://example.com/a-b here")
        self.assertIn('<a href="https://example.com/a-b">https://example.com/a-b</a>', html)

    def test_existing_links_untouched(self):
        html = render.render_markdown("[docs](https://example.com/doc)")
        self.assertEqual(html.count("<a"), 1)

    def test_code_block_untouched(self):
        html = render.render_markdown("```\nhttps://example.com/code\n```")
        self.assertIn("<pre>", html)
        self.assertNotIn("<a ", html)

    def test_trailing_punctuation_stripped(self):
        html = render.render_markdown("see https://example.com/note.")
        self.assertIn('<a href="https://example.com/note">', html)

    def test_relative_md_rewritten_to_content_route(self):
        html = render.render_markdown("[note](time-to-thought.md)", base_dir="knowledge")
        self.assertIn('href="/content/knowledge/time-to-thought.md"', html)

    def test_relative_md_resolved_against_base_dir(self):
        html = render.render_markdown(
            "[build](../builds/http-server.md)", base_dir="concepts"
        )
        self.assertIn('href="/content/builds/http-server.md"', html)

    def test_external_and_anchor_links_left_alone(self):
        html = render.render_markdown(
            "[anchor](#drill) and [ext](https://x.dev/a.md)", base_dir="concepts"
        )
        self.assertIn('href="#drill"', html)
        self.assertIn('href="https://x.dev/a.md"', html)

    def test_relative_link_to_missing_file_left_alone(self):
        html = render.render_markdown(
            "[ghost](nope.md)", base_dir="knowledge"
        )
        self.assertIn('href="nope.md"', html)


if __name__ == "__main__":
    unittest.main()

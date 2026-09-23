"""Observable search behavior, API failure handling, and credential hygiene."""
import contextlib
import importlib.util
import io
import json
import pathlib
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "search_issues", ROOT / "skills/sipeed-tang-mega-138k/scripts/search_issues.py")
search = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(search)


class SearchTests(unittest.TestCase):
    def test_bounded_results_include_prs_and_report_truncation(self):
        payload = {"total_count": 3, "incomplete_results": True, "items": [
            {"number": 1, "title": "clock", "html_url": "https://github.com/a/b/issues/1", "state": "closed"},
            {"number": 2, "title": "fix", "html_url": "https://github.com/a/b/pull/2", "state": "open", "pull_request": {}}]}
        def opener(request, timeout):
            self.assertEqual(timeout, 20)
            self.assertEqual(urllib.parse.urlsplit(request.full_url).hostname, "api.github.com")
            self.assertEqual(request.get_header("Authorization"), "Bearer private-token")
            self.assertNotIn("private-token", request.full_url)
            return io.StringIO(json.dumps(payload))
        result = search.fetch("repo:a/b clock", 2, "private-token", opener)
        self.assertTrue(result["truncated"])
        self.assertTrue(result["incomplete_results"])
        self.assertEqual([x["kind"] for x in result["items"]], ["issue", "pr"])

    def test_api_error_does_not_echo_response_or_token(self):
        def opener(request, timeout):
            raise urllib.error.HTTPError(request.full_url, 403, "private-token", {}, io.BytesIO(b"private-token"))
        with self.assertRaises(RuntimeError) as caught:
            search.fetch("repo:a/b clock", 2, "private-token", opener)
        self.assertIn("403", str(caught.exception))
        self.assertNotIn("private-token", str(caught.exception))

    def test_dry_run_never_fetches(self):
        with patch.object(search, "fetch", side_effect=AssertionError("network forbidden")), contextlib.redirect_stdout(io.StringIO()) as out:
            code = search.main(["--query", '"校准 failure"', "--dry-run", "--format", "json"])
        data = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(len(data["results"]), 2)
        self.assertIn('"校准 failure"', urllib.parse.parse_qs(urllib.parse.urlsplit(data["results"][0]["api_url"]).query)["q"][0])

    def test_networking_group_scopes_each_query_without_network(self):
        with patch.object(search, "fetch", side_effect=AssertionError("network forbidden")), contextlib.redirect_stdout(io.StringIO()) as out:
            code = search.main(["--group", "networking", "--query", "alignment", "--kind", "pr", "--dry-run", "--format", "json"])
        results = json.loads(out.getvalue())["results"]
        self.assertEqual(code, 0)
        self.assertEqual({r["repository"] for r in results}, {
            "enjoy-digital/liteeth", "enjoy-digital/litex_wr_nic",
            "key2/lambdaeth", "key2/gowin-serdes"})
        for result in results:
            query = urllib.parse.parse_qs(urllib.parse.urlsplit(result["api_url"]).query)["q"][0]
            self.assertEqual(query, f"repo:{result['repository']} alignment is:pr")

    def test_partial_failure_is_nonzero_and_keeps_success(self):
        ok = {"total_count": 0, "returned": 0, "truncated": False, "incomplete_results": False, "items": []}
        with patch.object(search, "fetch", side_effect=[RuntimeError("GitHub HTTP 429"), ok]), contextlib.redirect_stdout(io.StringIO()) as out:
            code = search.main(["--query", "PLL", "--format", "json"])
        data = json.loads(out.getvalue())
        self.assertEqual(code, 1)
        self.assertIn("error", data["results"][0])
        self.assertEqual(data["results"][1]["total_count"], 0)

    def test_invalid_responses_fail(self):
        for payload in ([], {"items": []}, {"items": [None], "total_count": 1}):
            with self.subTest(payload=payload), self.assertRaises(RuntimeError):
                search.fetch("repo:a/b clock", 2, opener=lambda *a, **k: io.StringIO(json.dumps(payload)))

    def test_scope_override_is_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            search.main(["--query", "repo:another/repo", "--dry-run"])
        self.assertEqual(caught.exception.code, 2)

    def test_literal_diagnostics_preserve_quotes_and_search_scope(self):
        for query in ('"PLL not locked"', '"NOT supported OR missing"',
                      '"repo:foo not found"', 'PLL not locked'):
            with self.subTest(query=query), patch.object(search, "fetch", side_effect=AssertionError("network forbidden")), contextlib.redirect_stdout(io.StringIO()) as out:
                code = search.main(["--query", query, "--dry-run", "--format", "json"])
            self.assertEqual(code, 0)
            result = json.loads(out.getvalue())["results"][0]
            self.assertEqual(result["query"], f"repo:sipeed/TangMega-138K-example {query}")

    def test_unquoted_scope_and_boolean_overrides_remain_rejected(self):
        for query in ('"PLL" OR repo:another/repo', 'org:another PLL',
                      'NOT PLL', '"unclosed'):
            with self.subTest(query=query), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                search.main(["--query", query, "--dry-run"])
            self.assertEqual(caught.exception.code, 2)

    def test_titles_cannot_inject_terminal_lines(self):
        self.assertNotIn("\x1b", search.clean("bad\x1b[31m\nnext"))
        self.assertNotIn("\n", search.clean("bad\nnext"))


if __name__ == "__main__":
    unittest.main()

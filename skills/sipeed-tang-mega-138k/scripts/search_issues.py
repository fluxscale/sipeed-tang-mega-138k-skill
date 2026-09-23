#!/usr/bin/env python3
"""Bounded, read-only public GitHub issue/PR search; Python standard library only."""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

GROUPS = {
    "boards": ["sipeed/TangMega-138K-example", "sipeed/TangMega-138KPro-example"],
    "tools": ["YosysHQ/apicula", "YosysHQ/nextpnr", "YosysHQ/yosys",
              "trabucayre/openFPGALoader"],
}


def repository(value):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
        raise argparse.ArgumentTypeError("repository must be OWNER/REPO")
    return value


def positive_limit(value):
    number = int(value)
    if not 1 <= number <= 100:
        raise argparse.ArgumentTypeError("limit must be between 1 and 100")
    return number


def make_query(repo, query, state="all", kind="all"):
    parts = [f"repo:{repo}", query.strip()]
    if state != "all":
        parts.append(f"state:{state}")
    if kind != "all":
        parts.append(f"is:{kind}")
    return " ".join(parts)


def search_url(query, limit):
    return "https://api.github.com/search/issues?" + urllib.parse.urlencode({
        "q": query, "per_page": limit, "sort": "updated", "order": "desc",
    })


def fetch(query, limit, token=None, opener=urllib.request.urlopen):
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "tang-mega-138k-skill-issue-search",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(search_url(query, limit), headers=headers)
    try:
        with opener(request, timeout=20) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        # Do not echo response bodies, request headers or credentials.
        advice = ""
        if exc.code in (403, 429):
            advice = " (rate limit or access restriction; retry later or check token permissions)"
        elif exc.code == 401:
            advice = " (authentication failed; check the configured token)"
        raise RuntimeError(f"GitHub HTTP {exc.code}{advice}") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise RuntimeError("GitHub network request failed or timed out") from None
    except (ValueError, UnicodeError):
        raise RuntimeError("GitHub returned an invalid JSON response") from None
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise RuntimeError("GitHub returned an unexpected search response")
    total = data.get("total_count")
    if not isinstance(total, int) or total < 0:
        raise RuntimeError("GitHub returned an invalid result count")
    items = []
    for item in data["items"][:limit]:
        if not isinstance(item, dict) or not all(
            key in item for key in ("number", "title", "html_url", "state")
        ):
            raise RuntimeError("GitHub returned an invalid result item")
        items.append({
            "number": item["number"], "title": item["title"],
            "url": item["html_url"], "state": item["state"],
            "kind": "pr" if "pull_request" in item else "issue",
            "updated_at": item.get("updated_at"),
        })
    return {"total_count": total, "returned": len(items),
            "truncated": total > len(items),
            "incomplete_results": bool(data.get("incomplete_results", False)),
            "items": items}


def clean(value):
    """Keep remote titles on one terminal line without control sequences."""
    return " ".join("".join(c if c.isprintable() else " " for c in str(value)).split())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--repo", type=repository, action="append", help="OWNER/REPO; repeatable")
    scope.add_argument("--group", choices=GROUPS, help="default: boards")
    parser.add_argument("--query", required=True, help="public keywords or quoted error; omit secrets")
    parser.add_argument("--state", choices=("all", "open", "closed"), default="all")
    parser.add_argument("--kind", choices=("all", "issue", "pr"), default="all")
    parser.add_argument("--limit", type=positive_limit, default=10, help="results per repository, 1–100")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--dry-run", action="store_true", help="show queries/URLs without network calls")
    args = parser.parse_args(argv)
    if not args.query.strip():
        parser.error("--query must not be empty")
    # Scope belongs to --repo/--group; keep user search terms from silently
    # expanding it through GitHub qualifiers or boolean expressions.
    if re.search(r"\b(?:repo|org|user):|\b(?:OR|NOT)\b", args.query, re.IGNORECASE):
        parser.error("use --repo/--group for scope; run alternative terms as separate queries")
    repos = list(dict.fromkeys(args.repo or GROUPS[args.group or "boards"]))
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    output = {"retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "dry_run": args.dry_run, "results": []}
    failed = False
    for repo in repos:
        query = make_query(repo, args.query, args.state, args.kind)
        result = {"repository": repo, "query": query,
                  "search_url": "https://github.com/search?" + urllib.parse.urlencode({"q": query, "type": "issues"})}
        if args.dry_run:
            result["api_url"] = search_url(query, args.limit)
        else:
            try:
                result.update(fetch(query, args.limit, token))
            except RuntimeError as exc:
                result["error"] = str(exc)
                failed = True
        output["results"].append(result)
    if args.format == "json":
        print(json.dumps(output, ensure_ascii=True, indent=2))
    else:
        print(f"Retrieved: {output['retrieved_at']} | dry-run: {args.dry_run}")
        for result in output["results"]:
            print(f"\n{result['repository']}\nQuery: {clean(result['query'])}")
            print(result["search_url"])
            if "error" in result:
                print(f"ERROR: {result['error']}")
            elif not args.dry_run:
                print(f"Returned {result['returned']} of {result['total_count']} | "
                      f"truncated: {result['truncated']} | incomplete: {result['incomplete_results']}")
                for item in result["items"]:
                    print(f"- {item['kind']} #{item['number']} ({clean(item['state'])}): "
                          f"{clean(item['title'])}\n  {clean(item['url'])}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

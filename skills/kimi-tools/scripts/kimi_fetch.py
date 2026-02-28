#!/usr/bin/env python3
"""Call Kimi coding fetch API and print JSON response."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid

FETCH_ENDPOINT = "https://api.kimi.com/coding/v1/fetch"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a page via Kimi coding API (POST /fetch).",
    )
    parser.add_argument("--url", required=True, help="Target URL to fetch.")
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=30,
        help="API timeout_seconds and HTTP timeout (default: 30).",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("KIMI_CODE_API_KEY"),
        help="Kimi API key. Defaults to env KIMI_CODE_API_KEY.",
    )
    parser.add_argument(
        "--tool-call-id",
        default=f"fetch-{uuid.uuid4().hex[:8]}",
        help="Value for X-Msh-Tool-Call-Id header.",
    )
    return parser.parse_args()


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    args = parse_args()

    if not args.api_key:
        fail("Missing API key. Set KIMI_CODE_API_KEY or pass --api-key.")

    if args.timeout_seconds <= 0:
        fail("--timeout-seconds must be > 0.")

    payload = {
        "url": args.url,
        "timeout_seconds": args.timeout_seconds,
    }

    request = urllib.request.Request(
        url=FETCH_ENDPOINT,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {args.api_key}",
            "Content-Type": "application/json",
            "X-Msh-Tool-Call-Id": args.tool_call_id,
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        fail(f"HTTP {exc.code} {exc.reason}\n{detail}")
    except urllib.error.URLError as exc:
        fail(f"Request failed: {exc.reason}")

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        fail(f"Response is not valid JSON:\n{body}")

    print(json.dumps(parsed, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

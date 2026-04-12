#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_REPO = "hyperbotsx/SoldierOne"
DEFAULT_PRS = (439, 440)
DEFAULT_PING_REVIEW_BODY = "@greptile"
PING_PREFIXES = ("@greptile", "@greptileai")
GREPTILE_LOGIN_HINT = "greptile"


@dataclass(frozen=True)
class Item:
    kind: str
    created_at: datetime
    author: str
    body: str
    url: str
    comment_id: int | None = None


@dataclass(frozen=True)
class Approval:
    comment_id: int
    comment_created_at: datetime
    reacted_at: datetime
    author: str
    url: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def default_state_dir() -> Path:
    return Path.cwd() / ".codex-local" / "greptile-monitor"


def run_gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def gh_json(args: list[str]) -> Any:
    stdout = run_gh(args)
    if not stdout.strip():
        return None
    return json.loads(stdout)


def fetch_items(repo: str, pr_number: int) -> list[Item]:
    issue_comments = gh_json(
        ["api", f"repos/{repo}/issues/{pr_number}/comments?per_page=100"]
    )
    reviews = gh_json(["api", f"repos/{repo}/pulls/{pr_number}/reviews?per_page=100"])
    review_comments = gh_json(
        ["api", f"repos/{repo}/pulls/{pr_number}/comments?per_page=100"]
    )

    items: list[Item] = []

    for row in issue_comments or []:
        created_at = parse_dt(row.get("created_at"))
        if created_at is None:
            continue
        items.append(
            Item(
                kind="issue_comment",
                created_at=created_at,
                author=(row.get("user") or {}).get("login", "unknown"),
                body=row.get("body") or "",
                url=row.get("html_url") or "",
                comment_id=row.get("id"),
            )
        )

    for row in reviews or []:
        created_at = parse_dt(row.get("submitted_at")) or parse_dt(row.get("created_at"))
        if created_at is None:
            continue
        items.append(
            Item(
                kind=f"review:{(row.get('state') or 'UNKNOWN').lower()}",
                created_at=created_at,
                author=(row.get("user") or {}).get("login", "unknown"),
                body=row.get("body") or "",
                url=row.get("html_url") or "",
            )
        )

    for row in review_comments or []:
        created_at = parse_dt(row.get("created_at")) or parse_dt(row.get("updated_at"))
        if created_at is None:
            continue
        path = row.get("path") or "unknown"
        line = row.get("line") or row.get("original_line")
        location = f"{path}:{line}" if line is not None else path
        items.append(
            Item(
                kind=f"review_comment:{location}",
                created_at=created_at,
                author=(row.get("user") or {}).get("login", "unknown"),
                body=row.get("body") or "",
                url=row.get("html_url") or "",
            )
        )

    items.sort(key=lambda item: item.created_at)
    return items


def is_greptile_author(author: str) -> bool:
    return GREPTILE_LOGIN_HINT in author.lower()


def is_ping_comment(item: Item) -> bool:
    if item.kind != "issue_comment":
        return False
    body = item.body.strip().lower()
    return any(body.startswith(prefix) for prefix in PING_PREFIXES)


def latest_ping_comment(items: list[Item]) -> Item | None:
    ping_comments = [item for item in items if is_ping_comment(item)]
    if not ping_comments:
        return None
    return max(ping_comments, key=lambda item: item.created_at)


def greptile_items_in_cycle(items: list[Item], ping_comment: Item | None) -> list[Item]:
    if ping_comment is None:
        return []
    return [
        item
        for item in items
        if is_greptile_author(item.author) and item.created_at > ping_comment.created_at
    ]


def fetch_latest_ping_approval(repo: str, ping_comment: Item | None) -> Approval | None:
    if ping_comment is None or ping_comment.comment_id is None:
        return None

    reactions = gh_json(
        [
            "api",
            f"repos/{repo}/issues/comments/{ping_comment.comment_id}/reactions?per_page=100",
        ]
    )

    approvals: list[Approval] = []
    for row in reactions or []:
        reacted_at = parse_dt(row.get("created_at"))
        if reacted_at is None:
            continue
        author = (row.get("user") or {}).get("login", "unknown")
        if row.get("content") != "+1" or not is_greptile_author(author):
            continue
        approvals.append(
            Approval(
                comment_id=ping_comment.comment_id,
                comment_created_at=ping_comment.created_at,
                reacted_at=reacted_at,
                author=author,
                url=ping_comment.url,
            )
        )

    if not approvals:
        return None
    return max(approvals, key=lambda approval: approval.reacted_at)


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"prs": {}}
    return json.loads(path.read_text())


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def write_log(path: Path, message: str) -> None:
    timestamp = iso(utc_now())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def trim_body(body: str, max_chars: int = 1000) -> str:
    body = body.strip()
    if len(body) <= max_chars:
        return body
    return body[:max_chars] + "\n... [truncated]"


def append_cycle_report(
    path: Path,
    pr_number: int,
    latest_greptile_at: datetime,
    cycle_items: list[Item],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## PR #{pr_number} review cycle ending {iso(latest_greptile_at)}\n\n"
        )
        if not cycle_items:
            handle.write("_No cycle items captured._\n")
            return
        for item in cycle_items:
            handle.write(
                f"- `{iso(item.created_at)}` `{item.kind}` `{item.author}` {item.url}\n"
            )
            body = trim_body(item.body)
            if body:
                handle.write("```text\n")
                handle.write(body)
                if not body.endswith("\n"):
                    handle.write("\n")
                handle.write("```\n")
        handle.write("\n")


def append_approval_report(path: Path, pr_number: int, approval: Approval) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n## PR #{pr_number} approval {iso(approval.reacted_at)}\n\n"
            f"- Greptile `+1` on ping comment `{approval.comment_id}` from {iso(approval.comment_created_at)}\n"
            f"- Comment URL: {approval.url}\n\n"
        )


def post_reping(repo: str, pr_number: int, ping_review_body: str, log_path: Path) -> None:
    run_gh(["pr", "comment", str(pr_number), "--repo", repo, "--body", ping_review_body])
    write_log(log_path, f"Posted {ping_review_body!r} to PR #{pr_number}")


def ensure_single_instance(pid_path: Path) -> None:
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    if pid_path.exists():
        raw = pid_path.read_text().strip()
        if raw:
            try:
                pid = int(raw)
                os.kill(pid, 0)
            except ProcessLookupError:
                pass
            except ValueError:
                pass
            else:
                raise RuntimeError(
                    f"Watcher is already running with pid {pid}. Remove {pid_path} if stale."
                )
    pid_path.write_text(str(os.getpid()) + "\n")


def cleanup_pid(pid_path: Path) -> None:
    try:
        if pid_path.exists():
            pid_path.unlink()
    except OSError:
        pass


def monitor_once(
    *,
    repo: str,
    prs: tuple[int, ...],
    ping_review_body: str,
    state_path: Path,
    log_path: Path,
    report_path: Path,
    settle_seconds: int,
) -> None:
    state = load_state(state_path)
    state.setdefault("prs", {})
    now = utc_now()

    for pr_number in prs:
        pr_key = str(pr_number)
        pr_state = state["prs"].setdefault(
            pr_key,
            {
                "last_logged_approval_at": None,
                "last_logged_greptile_at": None,
                "last_repinged_for_greptile_at": None,
            },
        )

        items = fetch_items(repo, pr_number)
        latest_ping = latest_ping_comment(items)
        latest_ping_at = latest_ping.created_at if latest_ping else None
        cycle_greptile_items = greptile_items_in_cycle(items, latest_ping)
        latest_greptile_at = max(
            (item.created_at for item in items if is_greptile_author(item.author)),
            default=None,
        )
        latest_approval = fetch_latest_ping_approval(repo, latest_ping)
        clean_approval = latest_approval is not None and not cycle_greptile_items

        last_logged_approval_at = parse_dt(pr_state.get("last_logged_approval_at"))
        last_logged_greptile_at = parse_dt(pr_state.get("last_logged_greptile_at"))
        last_repinged_for_greptile_at = parse_dt(
            pr_state.get("last_repinged_for_greptile_at")
        )

        if clean_approval and (
            last_logged_approval_at is None
            or latest_approval.reacted_at > last_logged_approval_at
        ):
            append_approval_report(report_path, pr_number, latest_approval)
            pr_state["last_logged_approval_at"] = iso(latest_approval.reacted_at)
            write_log(
                log_path,
                f"Captured Greptile approval on PR #{pr_number} via +1 reaction at {iso(latest_approval.reacted_at)}",
            )

        if latest_greptile_at and (
            last_logged_greptile_at is None or latest_greptile_at > last_logged_greptile_at
        ):
            cycle_floor = latest_ping_at
            cycle_items = [
                item
                for item in items
                if (cycle_floor is None or item.created_at > cycle_floor)
                and item.created_at <= latest_greptile_at
            ]
            append_cycle_report(report_path, pr_number, latest_greptile_at, cycle_items)
            pr_state["last_logged_greptile_at"] = iso(latest_greptile_at)
            write_log(
                log_path,
                f"Captured new Greptile cycle for PR #{pr_number} ending at {iso(latest_greptile_at)}",
            )

        if clean_approval:
            pr_state["current_cycle_status"] = "approved"
        elif cycle_greptile_items:
            pr_state["current_cycle_status"] = "reviewed_with_findings"
        elif latest_ping is not None:
            pr_state["current_cycle_status"] = "awaiting_review"
        else:
            pr_state["current_cycle_status"] = "not_pinged"

        if latest_greptile_at is None or clean_approval:
            continue

        review_has_settled = now - latest_greptile_at >= timedelta(seconds=settle_seconds)
        ping_is_stale = latest_ping_at is None or latest_ping_at < latest_greptile_at
        not_already_repinged = (
            last_repinged_for_greptile_at is None
            or latest_greptile_at > last_repinged_for_greptile_at
        )

        if review_has_settled and ping_is_stale and not_already_repinged:
            post_reping(repo, pr_number, ping_review_body, log_path)
            pr_state["last_repinged_for_greptile_at"] = iso(latest_greptile_at)
            pr_state["current_cycle_status"] = "repinged"

    state["last_run_at"] = iso(now)
    save_state(state_path, state)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Monitor GitHub PRs for Greptile comments, approvals, and re-review cycles."
    )
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--pr", type=int, action="append", dest="prs")
    parser.add_argument("--ping-body", default=DEFAULT_PING_REVIEW_BODY)
    parser.add_argument("--poll-seconds", type=int, default=120)
    parser.add_argument("--settle-seconds", type=int, default=600)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--state-dir", default=str(default_state_dir()))
    args = parser.parse_args()

    repo = args.repo
    prs = tuple(args.prs or DEFAULT_PRS)
    state_dir = Path(args.state_dir).resolve()
    state_path = state_dir / "state.json"
    log_path = state_dir / "watcher.log"
    report_path = state_dir / "review-cycles.md"
    pid_path = state_dir / "watcher.pid"

    if args.once:
        monitor_once(
            repo=repo,
            prs=prs,
            ping_review_body=args.ping_body,
            state_path=state_path,
            log_path=log_path,
            report_path=report_path,
            settle_seconds=args.settle_seconds,
        )
        return 0

    try:
        ensure_single_instance(pid_path)
        write_log(
            log_path,
            f"Starting watcher for PRs {', '.join(str(pr) for pr in prs)} in {repo}",
        )
        while True:
            try:
                monitor_once(
                    repo=repo,
                    prs=prs,
                    ping_review_body=args.ping_body,
                    state_path=state_path,
                    log_path=log_path,
                    report_path=report_path,
                    settle_seconds=args.settle_seconds,
                )
            except KeyboardInterrupt:
                raise
            except subprocess.CalledProcessError as exc:
                stderr = (exc.stderr or "").strip()
                write_log(
                    log_path,
                    f"gh command failed with exit code {exc.returncode}: {stderr}",
                )
            except Exception as exc:  # noqa: BLE001
                write_log(log_path, f"Unexpected error: {exc}")
            time.sleep(args.poll_seconds)
    except KeyboardInterrupt:
        write_log(log_path, "Watcher stopped by interrupt")
        return 130
    finally:
        cleanup_pid(pid_path)


if __name__ == "__main__":
    sys.exit(main())

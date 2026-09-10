#!/usr/bin/env python3
"""Write deploy-info.json at build time so the live commit is knowable.

Runs as part of the Vercel build command. Vercel exposes VERCEL_GIT_* env vars;
locally we fall back to git. Never raises — a stamping problem must not fail a
deploy that is otherwise fine.

    curl https://<site>/deploy-info.json    # what is actually live right now
"""
import json, os, subprocess, datetime, sys

def git(*a):
    try:
        return subprocess.run(["git", *a], capture_output=True, text=True,
                              timeout=10).stdout.strip() or None
    except Exception:
        return None

try:
    info = {
        "commit": os.environ.get("VERCEL_GIT_COMMIT_SHA") or git("rev-parse", "HEAD"),
        "branch": os.environ.get("VERCEL_GIT_COMMIT_REF") or git("rev-parse", "--abbrev-ref", "HEAD"),
        "message": os.environ.get("VERCEL_GIT_COMMIT_MESSAGE") or git("log", "-1", "--pretty=%s"),
        "repo": "/".join(filter(None, [os.environ.get("VERCEL_GIT_REPO_OWNER"),
                                       os.environ.get("VERCEL_GIT_REPO_SLUG")])) or None,
        "built_at": datetime.datetime.now(datetime.timezone.utc)
                        .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "env": os.environ.get("VERCEL_ENV") or "local",
    }
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "deploy-info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)
        f.write("\n")
    print(f"stamped deploy-info.json: {info['commit'] and info['commit'][:8]} "
          f"({info['branch']}, {info['env']})")
except Exception as e:                      # never fail the build over a stamp
    print(f"stamp-build: skipped ({e})", file=sys.stderr)

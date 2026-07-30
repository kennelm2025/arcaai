"""B7 inc4-b operator CLI: governed end-to-end agent run.

Composition root (ADR-0009): constructs the ChromaStore adapter over
the persistent corpus index, opens the root governed_request on the
runtime (app) role, invokes the agent graph inside it, then reads the
run's events back via events_for_run and prints the transcript - the
CF-1/B7-c evidence block. The retrieve-leg latency (state
retrieval_ms) is printed for CF-1/B7-d transcription into B7_GATE -
recorded, not gated.

Dry-run by default (house rule): --live executes; the default prints
the resolved configuration and exits without constructing the store
or touching the database. Audit rows on the dev stack are wiped by
the governance suite's session fixtures (drop_all/create_all) - the
printed transcript, not the rows, is the durable evidence.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "verticals" / "fraud" / "corpus" / "MANIFEST.yaml"
INDEX_PATH = REPO_ROOT / "data" / "fraud" / "corpus_index"

# Same env override and dev default as tests/governance/conftest.py -
# runtime role, never owner: the runner is a consumer of the grants,
# not an administrator of the schema.
APP_DSN = os.environ.get(
    "ARCAAI_AUDIT_APP_DSN",
    "postgresql+psycopg://arcaai_app:app_dev@localhost:5432/arcaai_audit",
)


def read_manifest_version() -> str:
    import yaml

    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh)
    version = manifest.get("manifest_version")
    if not version:
        raise SystemExit(f"manifest_version missing from {MANIFEST_PATH}")
    return str(version)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="B7 governed end-to-end agent run (inc4-b)"
    )
    parser.add_argument(
        "--live", action="store_true", help="execute (default: dry run)"
    )
    parser.add_argument("--live-scoring", action="store_true")
    parser.add_argument("--live-packaging", action="store_true")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--query", default=None, help="override the fixture query"
    )
    args = parser.parse_args()

    manifest_version = read_manifest_version()

    print(f"manifest_version : {manifest_version}")
    print(f"corpus index     : {INDEX_PATH}")
    print(f"audit DSN (host) : {APP_DSN.split('@')[-1]}")
    print(f"top_k            : {args.top_k}")
    print(
        "live flags       : "
        f"scoring={args.live_scoring} packaging={args.live_packaging}"
    )
    if not args.live:
        print("dry run - pass --live to execute")
        return

    sys.path.insert(0, str(REPO_ROOT))

    from sqlalchemy import create_engine

    from agent.fixtures import INTAKE_FIXTURE
    from agent.graph import build_graph
    from arcaai.platform.governance.audit import AuditStore
    from arcaai.platform.governance.wrapper import governed_request
    from arcaai.platform.retrieval.chroma_store import ChromaStore

    retrieval_store = ChromaStore(persist_directory=str(INDEX_PATH))
    print(f"index chunks     : {retrieval_store.count()}")

    audit = AuditStore(create_engine(APP_DSN))
    state = dict(INTAKE_FIXTURE)
    if args.query:
        state["query"] = args.query

    graph = build_graph(
        live_scoring=args.live_scoring,
        live_packaging=args.live_packaging,
        live_retrieval=True,
        retrieval_store=retrieval_store,
        manifest_version=manifest_version,
        retrieval_top_k=args.top_k,
    )

    with governed_request(
        audit,
        source="scripts/b7_run.py",
        corpus_version=manifest_version,
        retrieval_config={"top_k": args.top_k, "index": str(INDEX_PATH)},
    ) as ctx:
        out = graph.invoke(state)
        correlation_id = ctx.correlation_id

    print()
    print("=== governed run transcript (CF-1/B7-c evidence) ===")
    print(f"correlation_id : {correlation_id}")
    for event in audit.events_for_run(correlation_id):
        payload = event.payload or {}
        line = f"seq {event.sequence_number}  {event.event_type}"
        if event.event_type == "retrieval_performed":
            line += (
                f"  manifest_version={payload.get('manifest_version')}"
                f"  top_k={payload.get('top_k')}"
                f"  result_count={payload.get('result_count')}"
            )
        print(line)
        if event.event_type == "retrieval_performed":
            for cid in payload.get("chunk_ids", []):
                print(f"    chunk {cid}")
    print()
    print(f"score          : {out.get('score')}")
    print(
        f"retrieval_ms   : {out.get('retrieval_ms'):.1f}  "
        "(CF-1/B7-d - transcribe to B7_GATE)"
    )
    print(f"narrative      : {str(out.get('narrative', ''))[:200]}")


if __name__ == "__main__":
    main()

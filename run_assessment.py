"""
run_assessment.py — Run all 5 assessment questions and save results.

Outputs:
    outputs/results.json  — structured JSON with all answers
    outputs/results.txt   — human-readable formatted report

Usage:
    python run_assessment.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from rag import answer

# ─── Assessment Questions ─────────────────────────────────────────────────────
QUESTIONS: list[dict] = [
    {
        "id": "Q1",
        "question": (
            "I have 72% attendance this semester. How many attendance marks will I receive, "
            "and am I eligible to appear for the final examination?"
        ),
    },
    {
        "id": "Q2",
        "question": (
            "Within how many days after recovery must a student submit supporting documents "
            "for Medical Leave? What happens if the documents are submitted after this period?"
        ),
    },
    {
        "id": "Q3",
        "question": (
            "What is the monthly subscription fee for using the campus swimming pool "
            "and indoor squash court?"
        ),
    },
    {
        "id": "Q4",
        "question": (
            "What minimum percentage of batch-student support is required to propose a new "
            "student club, and which authority reviews the proposal first?"
        ),
    },
    {
        "id": "Q5",
        "question": (
            "What is the default WPA2 password for the Mirai_Student_5G campus Wi-Fi network?"
        ),
    },
]


def format_sources(sources: list[int]) -> str:
    """Format sources list for human-readable output."""
    if not sources:
        return "N/A"
    return ", ".join(f"page {p}" for p in sources)


def run_all() -> list[dict]:
    """Execute each question and collect responses."""
    results: list[dict] = []
    total = len(QUESTIONS)

    print("=" * 70)
    print("University Academic & Hostel Policy Advisor — Assessment")
    print("=" * 70)

    for i, item in enumerate(QUESTIONS, start=1):
        qid = item["id"]
        q_text = item["question"]
        print(f"\n[{i}/{total}] {qid}: {q_text}")

        t0 = time.time()
        try:
            res = answer(q_text)
            ans = res["answer"]
            src = res["sources"]
        except Exception as exc:
            ans = f"[ERROR] {exc}"
            src = []

        elapsed = time.time() - t0

        record = {
            "id": qid,
            "question": q_text,
            "answer": ans,
            "sources": src,
            "latency_s": round(elapsed, 2),
        }
        results.append(record)

        print(f"  Answer : {ans}")
        print(f"  Sources: {format_sources(src)}")
        print(f"  Latency: {elapsed:.2f}s")

    return results


def save_json(results: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[output] JSON saved → {path}")


def save_txt(results: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "=" * 70,
        "UNIVERSITY ACADEMIC & HOSTEL POLICY ADVISOR — RAG ASSESSMENT",
        "=" * 70,
        "",
    ]

    for r in results:
        lines.append(f"┌─ {r['id']}")
        lines.append(f"│  Q: {r['question']}")
        lines.append(f"│  A: {r['answer']}")
        lines.append(f"│  Sources: {format_sources(r['sources'])}")
        lines.append(f"│  Latency: {r['latency_s']}s")
        lines.append("└" + "─" * 68)
        lines.append("")

    lines.append("=" * 70)
    lines.append(f"Total questions: {len(results)}")
    answered = sum(1 for r in results if r["answer"] != "[not found]" and not r["answer"].startswith("[ERROR]"))
    not_found = sum(1 for r in results if r["answer"] == "[not found]")
    errors = sum(1 for r in results if r["answer"].startswith("[ERROR]"))
    lines.append(f"Answered: {answered}  |  Not found: {not_found}  |  Errors: {errors}")
    lines.append("=" * 70)

    text = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[output] TXT  saved → {path}")


def main() -> None:
    results = run_all()
    save_json(results, Path("outputs/results.json"))
    save_txt(results, Path("outputs/results.txt"))
    print("\n[done] Assessment execution complete.")


if __name__ == "__main__":
    main()

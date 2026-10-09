#!/usr/bin/env python3
"""Said-twice — Jev decides what stays in the transcript, and escalates what it is not sure about.

  python3 said_twice_check.py <project>            # the built cut -> review/said_twice.json   (default)
  python3 said_twice_check.py <project> --raw      # the raw camera transcript, before targets.py
  python3 said_twice_check.py <project> --raw --decide   # also write the drop-list the voice cut consumes

WHAT IT DECIDES, AND WHAT IT NEVER TOUCHES
It answers one question over the transcript — **is this line already said?** — and that is a decision about what is
included, not a summary. With `--decide` the clear cases become a drop-list (`edit/jev_drops.json`) that feeds the
voice cut: the EARLIER of a duplicated pair goes, which is the existing "last take wins" rule (cutting.md §3).
The uncertain band is never decided automatically — it is escalated to the mediator, by design.

It does NOT write the transcript. The words come from speech-to-text; Jev is text-only and never hears the audio.
It also never moves a cut point: those stay on RMS troughs, in code. Jev judges content, code owns the timeline.

WHY IT EARNS ITS PLACE
Pass B is a 5-gram slide. It catches a verbatim repeat and misses a paraphrased one: "We have some API key stuff
going on" and "Then we have some API keys, some documentation" are the same line twice and share no 5-gram
(cutting.md §3.7 records both of these from a real recording). Judging "do these say the same thing?" is semantics,
not string overlap, so it goes to Jev, which returns a calibrated probability instead of prose.

COST AND SHAPE (https://docs.typesafe.ai/api.md)
State carries the sentences once; every neighbouring pair inside a 30 s / 6-sentence window is one Noul; Jev reads
the state once and answers them all in parallel. A 22-minute recording is ~3.5k tokens of transcript — fractions of
a cent at $0.042 / M input.

NO KEY, NO PROBLEM
Without TYPESAFE_API_KEY the check SKIPS with a message and exits 0. It is an extra pair of eyes, not a dependency:
the pipeline and the 5-gram Pass B run exactly as before.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from pathlib import Path
import urllib.request, urllib.error

API, MODEL = "https://api.typesafe.ai/v1/systemone", "jev-latest"
FLAG, CLEAR = 0.85, 0.35        # >=FLAG decided: drop the earlier · <=CLEAR decided: keep both
                                # between the two = NOT decided here, escalated to the mediator
WINDOW_S, WINDOW_N, CHUNK = 30.0, 6, 40


def api_key():
    for p in (Path.cwd() / ".env", Path.home() / ".env"):
        if p.exists():
            for line in p.read_text().splitlines():
                if line.startswith("TYPESAFE_API_KEY="):
                    v = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if v:
                        return v
    return os.environ.get("TYPESAFE_API_KEY") or None


def ask(state, questions, key, retries=4):
    body = json.dumps({"state": state, "model": MODEL, "questions": questions}).encode()
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for a in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and a < retries - 1:
                time.sleep(2 ** a); continue
            print(f"  said-twice check: TypeSafe {e.code} — skipping (the cut is unaffected)", file=sys.stderr)
            return None
        except Exception:
            if a < retries - 1:
                time.sleep(2 ** a); continue
            print("  said-twice check: TypeSafe unreachable — skipping (the cut is unaffected)", file=sys.stderr)
            return None


def sentences(words):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        gap = (words[i + 1]["start"] - w["end"]) if i + 1 < len(words) else 9
        if (w["text"].rstrip('"”').endswith((".", "?", "!")) and gap > 0.08) or gap > 0.55 or i == len(words) - 1:
            out.append({"start": round(cur[0]["start"], 2), "end": round(cur[-1]["end"], 2),
                        "sec": cur[0].get("sec", ""), "text": " ".join(x["text"] for x in cur)})
            cur = []
    return out


def said_twice_q(a, b):
    """One condition, affirmative phrasing, criteria only where the boundary is genuinely ambiguous
    (https://docs.typesafe.ai/primitives/noul.md)."""
    return {"type": "noul",
            "instructions": f"`sentences[{a}].text` and `sentences[{b}].text` say the same thing twice — the "
                            f"viewer would hear the same point made a second time.",
            "criteria": {
                "true": "Both make the same point, even in completely different words, and the second adds no new "
                        "fact. Includes a fuller re-phrasing of the same sentence, and a second attempt that "
                        "finishes a thought the first one broke off.",
                "false": "The second advances the video — it adds a new fact, number, name or example, or answers "
                         "something the first one set up. Deliberate repetition for emphasis, and two different "
                         "points that merely share wording, are NOT the same thing said twice."}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project"); ap.add_argument("--raw", action="store_true")
    ap.add_argument("--decide", action="store_true", help="also write edit/jev_drops.json for the voice cut")
    a = ap.parse_args()
    P = Path(a.project).resolve()

    key = api_key()
    if not key:
        print("said-twice check: no TYPESAFE_API_KEY — skipping. This is an EXTRA check; the 5-gram Pass B in\n"
              "                  cutting.md §4 still runs and the cut is unaffected.")
        return 0

    if a.raw:
        words = [w for w in json.load(open(P / "edit/raw/transcripts/cam.json"))["words"] if w["type"] == "word"]
        for w in words:
            if w["end"] - w["start"] > 0.9:
                w["start"] = w["end"] - 0.45
        out_path = P / "review/said_twice_raw.json"
    else:
        words, off = [], 0.0
        for d in sorted((P / "sections").iterdir()):
            t = d / "transcript.json"
            if not t.exists():
                continue
            ws = [w for w in json.load(open(t))["words"] if w["type"] == "word"]
            for w in ws:
                w["start"] += off; w["end"] += off; w["sec"] = d.name
            words += ws
            off = words[-1]["end"] + 0.5
        out_path = P / "review/said_twice.json"

    sents = sentences(words)
    print(f"said-twice check: {len(sents)} sentences through {MODEL}")

    flagged, uncertain, usage, asked = [], [], {"input_tokens": 0, "output_tokens": 0}, 0
    for c0 in range(0, len(sents), CHUNK):
        chunk = sents[c0:c0 + CHUNK + WINDOW_N]
        qs = {}
        for li, s in enumerate(chunk):
            if c0 + li >= c0 + CHUNK:
                break
            for lj in range(li + 1, min(li + 1 + WINDOW_N, len(chunk))):
                if chunk[lj]["start"] - s["end"] > WINDOW_S:
                    break
                qs[f"d_{c0+li}_{c0+lj}"] = said_twice_q(li, lj)
        if not qs:
            continue
        r = ask({"sentences": [{"text": s["text"]} for s in chunk]}, qs, key)
        if r is None:
            return 0                      # degrade quietly; never block the pipeline
        asked += len(qs)
        for k in usage:
            usage[k] += r.get("usage", {}).get(k, 0)
        for k, v in r["answers"].items():
            _, i, j = k.split("_"); i, j = int(i), int(j)
            p = v["noul"]
            row = {"p": round(p, 3), "a_t": sents[i]["start"], "b_t": sents[j]["start"],
                   "a_sec": sents[i]["sec"], "b_sec": sents[j]["sec"],
                   "a": sents[i]["text"], "b": sents[j]["text"]}
            if p >= FLAG: flagged.append(row)
            elif p > CLEAR: uncertain.append(row)

    flagged.sort(key=lambda r: -r["p"]); uncertain.sort(key=lambda r: -r["p"])
    cost = usage["input_tokens"] / 1e6 * 0.042
    json.dump({"model": MODEL, "sentences": len(sents), "pairs_checked": asked,
               "flagged": flagged, "uncertain": uncertain, "usage": usage, "cost_usd": round(cost, 5),
               "thresholds": {"said_twice": FLAG, "clear": CLEAR}},
              open(out_path, "w"), indent=1)

    if a.decide:
        drops=[{"drop_start": r["a_t"], "drop_end": sents[0]["end"] if False else None, "p": r["p"],
                "dropped_text": r["a"], "kept_text": r["b"], "kept_start": r["b_t"]} for r in flagged]
        (P/"edit").mkdir(exist_ok=True)
        json.dump({"model": MODEL, "rule": "last take wins - the EARLIER of a duplicated pair is dropped",
                   "threshold": FLAG, "decided": drops, "escalated": uncertain},
                  open(P/"edit/jev_drops.json","w"), indent=1)
        print(f"  --decide: {len(drops)} drops -> edit/jev_drops.json ({len(uncertain)} escalated to you)")
    print(f"  {asked} pairs checked · {len(flagged)} decided as said twice · {len(uncertain)} escalated · "
          f"{usage['input_tokens']} tokens = ${cost:.5f}")
    for r in flagged:
        print(f"  [{r['p']:.2f}] {r['a_sec']} {r['a_t']:6.1f}  {r['a'][:62]}")
        print(f"         {r['b_sec']} {r['b_t']:6.1f}  {r['b'][:62]}")
    if not flagged:
        print("  nothing is said twice.")
    print(f"  -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

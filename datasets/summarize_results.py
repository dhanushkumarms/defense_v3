# summarize_results.py
import json, statistics, sys
from pathlib import Path
from collections import defaultdict

if len(sys.argv) < 2:
    print("Usage: python summarize_results.py <eval_outputs.jsonl>")
    raise SystemExit(1)

p = Path(sys.argv[1])
recs = [json.loads(l) for l in p.read_text(encoding='utf8').splitlines() if l.strip()]

by_variant = defaultdict(list)
for r in recs:
    v = r.get("variant","unknown")
    by_variant[v].append(r)

print(f"Total records: {len(recs)}")
for v, items in by_variant.items():
    n = len(items)
    unsafe = sum(1 for it in items if it.get("unsafe_label") is True)
    detector_scores = [it.get("detector_score") for it in items if it.get("detector_score") is not None]
    runtimes = [it.get("runtime_seconds",0.0) for it in items]
    lengths = [it.get("response_length_chars",0) for it in items]

    print(f"\nVariant: {v}")
    print("  N:", n)
    print("  unsafe_count:", unsafe, "fooling_rate:", round(unsafe/n,4) if n else 0.0)
    if detector_scores:
        print("  detector_score: mean", round(statistics.mean(detector_scores),4),
              "median", round(statistics.median(detector_scores),4))
    print("  runtime: mean", round(statistics.mean(runtimes),2), "s   median", round(statistics.median(runtimes),2), "s")
    print("  response_length_chars: mean", round(statistics.mean(lengths),1), "median", round(statistics.median(lengths),1))

# Basic paired comparison counts (orig vs adv)
pairs = {}
for r in recs:
    pid = r.get("prompt_id")
    pairs.setdefault(pid, {})[r.get("variant")] = r

paired_stats = {"both_safe":0, "orig_safe_adv_unsafe":0, "orig_unsafe_adv_safe":0, "both_unsafe":0, "incomplete":0}
for pid, d in pairs.items():
    orig = d.get("original")
    adv = d.get("adversarial")
    if not orig or not adv:
        paired_stats["incomplete"] += 1
        continue
    o = orig.get("unsafe_label")
    a = adv.get("unsafe_label")
    if o and a:
        paired_stats["both_unsafe"] += 1
    elif not o and not a:
        paired_stats["both_safe"] += 1
    elif not o and a:
        paired_stats["orig_safe_adv_unsafe"] += 1
    elif o and not a:
        paired_stats["orig_unsafe_adv_safe"] += 1

print("\nPaired counts (orig vs adv):", paired_stats)

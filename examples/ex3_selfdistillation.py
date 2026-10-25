"""Example 3. Self-distillation with known ground truth, one stated failure mode.

Setup (all conditions stated): a model is a distribution q over K correct items
(truth p, a 1/rank law) and M wrong items. Each generation draws N samples from q
and refits q to the counts of whatever samples survive. No fresh data enters
unless a condition says so. Selection, training and evaluation are separate steps:

  train_only      refit on all N samples.
  confidence_sel  keep only samples whose current probability is in the top 75%.
  posthoc_eval    train_only plus a metric read each generation. Evaluation here
                  measures the result and does not touch the trajectory.
  verifier_loop   a verifier rejects wrong items before refitting (evaluation
                  that changes selection, which is corrective control).
  verifier_anchor verifier_loop plus N//10 verified fresh samples from truth.

Stated failure mode: coverage of correct items shrinks under finite sampling
without fresh data. A verifier establishes that each retained item is correct;
it does not establish that the retained set is representative.
"""
import random
from collections import Counter

K, M, N, GENS, SEEDS = 30, 10, 100, 40, 20
raw = [1 / (i + 1) for i in range(K)]
truth = [x / sum(raw) for x in raw]
Q0 = [0.92 * t for t in truth] + [0.08 / M] * M


def draw(q, rng, n):
    return rng.choices(range(K + M), weights=q, k=n)


def refit(items, q):
    if not items:
        return q
    c = Counter(items)
    return [c[i] / len(items) for i in range(K + M)]


def metrics(q):
    cov = sum(q[i] > 0 for i in range(K)) / K
    err = sum(q[K:])
    tv = 0.5 * sum(abs(q[i] - (truth[i] if i < K else 0.0)) for i in range(K + M))
    return cov, err, tv


def run(cond, seed):
    rng, q, log = random.Random(seed), Q0, []
    for _ in range(GENS):
        s = draw(q, rng, N)
        if cond == "confidence_sel":
            cut = sorted(q[i] for i in s)[N // 4]
            s = [i for i in s if q[i] >= cut]
        if cond in ("verifier_loop", "verifier_anchor"):
            s = [i for i in s if i < K]
        if cond == "verifier_anchor":
            s += rng.choices(range(K), weights=truth, k=N // 10)
        q = refit(s, q)
        if cond == "posthoc_eval":
            log.append(metrics(q))
    return q, log


def mean_final(cond):
    rows = [metrics(run(cond, sd)[0]) for sd in range(SEEDS)]
    return [sum(r[j] for r in rows) / SEEDS for j in range(3)]


print(f"K={K} correct, M={M} wrong, N={N} samples/generation, {GENS} generations, {SEEDS} seeds")
print(f"start: coverage 1.000, wrong mass 0.080, TV {metrics(Q0)[2]:.3f}")
print(f"{'condition':<17}{'coverage':>10}{'wrong mass':>12}{'TV to truth':>13}")
res = {}
for cond in ["train_only", "confidence_sel", "posthoc_eval", "verifier_loop", "verifier_anchor"]:
    res[cond] = mean_final(cond)
    print(f"{cond:<17}{res[cond][0]:>10.3f}{res[cond][1]:>12.3f}{res[cond][2]:>13.3f}")

same = all(run("train_only", sd)[0] == run("posthoc_eval", sd)[0] for sd in range(SEEDS))
print()
print("posthoc_eval trajectory identical to train_only on every seed:", same)
assert same
assert res["train_only"][0] < 0.95 and res["verifier_loop"][0] < 0.95
assert res["verifier_loop"][1] == 0.0
assert res["verifier_anchor"][0] > res["verifier_loop"][0]
print("Checks passed: coverage falls without fresh data, the verifier removes wrong")
print("mass but leaves coverage falling, and anchoring with fresh verified samples helps.")
print("These hold under the stated conditions only; none of this is claimed in general.")

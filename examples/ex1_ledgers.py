"""Example 1. Proposition 5: inscription counts underdetermine warranted content.

A ledger is a list of inscriptions (id, kind, cites). The fixed procedure P is
grounded closure: an observation has standing; a derived item has standing if and
only if it cites at least one item and every item it cites has standing. P is
deliberately simple. The point is structural, not a claim about any real procedure.
"""
from itertools import combinations, product
from collections import defaultdict


def standing(ledger):
    good = {i for i, k, _ in ledger if k == "obs"}
    changed = True
    while changed:
        changed = False
        for i, k, c in ledger:
            if k == "claim" and i not in good and c and all(x in good for x in c):
                good.add(i)
                changed = True
    return good


def signature(ledger):
    """Everything a count-based summary could see: size, observations, citation links."""
    return (len(ledger),
            sum(k == "obs" for _, k, _ in ledger),
            sum(len(c) for _, _, c in ledger))


# Two ledgers with the same size, the same number of observations, and the same
# number of citation links. They differ only in how the citations are arranged.
A = [(1, "obs", ()), (2, "obs", ()), (3, "claim", (1,)),
     (4, "claim", (1, 2)), (5, "claim", (3,)), (6, "claim", (4, 5))]
B = [(1, "obs", ()), (2, "obs", ()), (3, "claim", (4,)),
     (4, "claim", (3, 1)), (5, "claim", (6,)), (6, "claim", (5, 2))]

print("Ledger A: signature", signature(A), "standing", sorted(standing(A)))
print("Ledger B: signature", signature(B), "standing", sorted(standing(B)))
assert signature(A) == signature(B)
assert standing(A) != standing(B)


def all_ledgers(n):
    ids = list(range(n))
    options = []
    for i in ids:
        others = [j for j in ids if j != i]
        opts = [(i, "obs", ())]
        for r in range(1, len(others) + 1):
            opts += [(i, "claim", c) for c in combinations(others, r)]
        options.append(opts)
    return product(*options)


n = 4
by_sig = defaultdict(set)
total = 0
for ledger in all_ledgers(n):
    total += 1
    by_sig[signature(ledger)].add(len(standing(ledger)))

ambiguous = {s: v for s, v in by_sig.items() if len(v) > 1}
print()
print(f"All {total} ledgers with {n} inscriptions (inscription count is {n} for every one):")
print("  standing sizes seen across all of them:", sorted({x for v in by_sig.values() for x in v}))
print(f"  signature classes (size, observations, links): {len(by_sig)}")
print(f"  classes whose members differ in how many items have standing: {len(ambiguous)}")
worst = max(ambiguous.items(), key=lambda kv: (len(kv[1]), kv[0]))
print(f"  example class {worst[0]} has standing sizes {sorted(worst[1])}")
assert ambiguous, "claim fails: counts would determine standing size"
print()
print("Result: no function of inscription count, observation count, or link count")
print("determines the warranted content of the record.")

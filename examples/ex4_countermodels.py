"""Example 4. Countermodels for Proposition 1 and for the consequence and scope
cases of Proposition 2, found by exhaustive search over small systems.

Part A. A rule system gives each of five operations a set of prerequisite
operations drawn from the earlier ones. A trace is a sequence of operations. An
operation occurs when it appears in the trace. It is licensed at that point when
its prerequisites have already occurred. Occurrence and licensing are separate.

Part B. Contexts are 0..3. Evidence V assigns 0, 1 or nothing to each context. A
candidate is a function h from contexts to {0, 1}. The fixed procedure P gives h
standing for consequence level c in scope S when h agrees with V on every observed
context in S and at least c contexts in S are observed.
"""
from itertools import chain, combinations, product

OPS = ["generate", "inscribe", "evaluate", "authorize", "commit"]


def subsets(xs):
    return chain.from_iterable(combinations(xs, r) for r in range(len(xs) + 1))


def licensed(rules, trace):
    done = set()
    for op in trace:
        if not set(rules[op]) <= done:
            return False
        done.add(op)
    return True


systems = [dict(zip(OPS, choice)) for choice in
           product(*[list(subsets(OPS[:i])) for i in range(len(OPS))])]
traces = [t for n in range(6) for t in product(OPS, repeat=n)]

occurs_unlicensed = sum(1 for R in systems for t in traces
                        if "commit" in t and not licensed(R, t))
licensed_not_occurring = sum(1 for R in systems for t in traces
                             if licensed(R, t) and "commit" not in t
                             and set(R["commit"]) <= set(t))
req = [R for R in systems if "evaluate" in R["commit"]]
nonreq = [R for R in systems if "evaluate" not in R["commit"]]
leak_req = sum(1 for R in req for t in traces if licensed(R, t)
               and "commit" in t and "evaluate" not in t[:t.index("commit")])
leak_nonreq = sum(1 for R in nonreq for t in traces if licensed(R, t)
                  and "commit" in t and "evaluate" not in t[:t.index("commit")])
print(f"Part A: {len(systems)} rule systems, {len(traces)} traces each")
print(f"  commit occurs in an unlicensed trace:                      {occurs_unlicensed} cases")
print(f"  commit licensed at the end of a trace and never occurs:    {licensed_not_occurring} cases")
print(f"  rules requiring evaluation: licensed commits without prior evaluation:    {leak_req}")
print(f"  rules not requiring evaluation: licensed commits without prior evaluation: {leak_nonreq}")
assert occurs_unlicensed > 0 and licensed_not_occurring > 0
assert leak_req == 0 and leak_nonreq > 0
print("  Occurrence does not entail licensing. Where the rules require evaluation, no")
print("  licensed trace commits without it. Where they do not, the rules are defective.")

CTX = range(4)


def has_standing(h, V, S, c):
    seen = [x for x in S if V[x] is not None]
    return len(seen) >= c and all(h[x] == V[x] for x in seen)


Vs = list(product([None, 0, 1], repeat=4))
hs = list(product([0, 1], repeat=4))
scopes = [s for s in subsets(CTX) if s]
size = lambda V: sum(v is not None for v in V)

cons = [(size(V), V, h, S, c1, c2) for V in Vs for h in hs for S in scopes
        for c1 in (1, 2) for c2 in (c1 + 1, 3) if c2 > c1
        and has_standing(h, V, S, c1) and not has_standing(h, V, S, c2)]
scope_lost = [(size(V) + len(S2), V, h, S1, S2, c) for V in Vs for h in hs
              for S1 in scopes for S2 in scopes if set(S1) < set(S2) for c in (1, 2, 3)
              if has_standing(h, V, S1, c) and not has_standing(h, V, S2, c)]
scope_gain = sum(1 for V in Vs for h in hs for S1 in scopes for S2 in scopes
                 if set(S1) < set(S2) for c in (1, 2, 3)
                 if not has_standing(h, V, S1, c) and has_standing(h, V, S2, c))
cons_gain = sum(1 for V in Vs for h in hs for S in scopes for c in (1, 2)
                if not has_standing(h, V, S, c) and has_standing(h, V, S, c + 1))
print()
print("Part B: standing is not generally preserved (one fixed procedure, fixed evidence)")
key = lambda r: (r[0], str(r[1:]))
m = min(cons, key=key)
print(f"  consequence {m[4]} -> {m[5]}: {len(cons)} losses; smallest: V={m[1]}, h={m[2]}, scope={m[3]}")
m = min(scope_lost, key=key)
print(f"  scope widening: {len(scope_lost)} losses; smallest: V={m[1]}, h={m[2]}, "
      f"scope {m[3]} -> {m[4]}, level {m[5]}")
print(f"  raising consequence never gains standing here: {cons_gain} gains")
print(f"  widening scope can gain standing here (more contexts observed): {scope_gain} gains")
assert cons and scope_lost and cons_gain == 0 and scope_gain > 0
print("  Standing is not monotone in consequence or scope, and the scope direction runs")
print("  both ways. The commitments dimension is the state-indexed model in Example 2.")

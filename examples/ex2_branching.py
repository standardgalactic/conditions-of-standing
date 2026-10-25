"""Example 2. Commitments countermodel for Proposition 2.

A transition is a state-indexed object (s, op, s'). The proposed operation is a
history rewrite that squashes a branch into one commit. The evidence V is whether
the rewrite leaves the final tree unchanged. The procedure P accepts a rewrite
when V holds and the rewrite does not remove any commit that is already
published. The set of published commits is the commitment set K. The same
operation with the same evidence is assessed in different states.
"""


def make_state(published=()):
    return {"commits": {"base": ((), "T0"), "c1": (("base",), "T1"),
                        "c2": (("c1",), "T2"), "c3": (("c2",), "T3")},
            "branches": {"feature": "c3"},
            "published": frozenset(published)}


def path(state, branch, stop):
    out, cur = [], state["branches"][branch]
    while cur != stop:
        out.append(cur)
        cur = state["commits"][cur][0][0]
    return out


def apply(state, op):
    _, branch, base = op
    removed = path(state, branch, base)
    head_tree = state["commits"][removed[0]][1]
    commits = {k: v for k, v in state["commits"].items() if k not in removed}
    commits["sq"] = ((base,), head_tree)
    branches = dict(state["branches"], **{branch: "sq"})
    return dict(state, commits=commits, branches=branches), set(removed)


def tree_of(state, branch):
    return state["commits"][state["branches"][branch]][1]


def std_stateless(op, before, after):
    """The candidate assessed on evidence V alone, as if standing belonged to the candidate."""
    return tree_of(before, op[1]) == tree_of(after, op[1])


def std(state, op):
    """Standing of the transition (state, op, state') under V, P and K = state['published']."""
    after, removed = apply(state, op)
    return std_stateless(op, state, after) and not (removed & state["published"])


op = ("squash", "feature", "base")
print("Candidate operation:", op, "(same evidence in every row: final tree unchanged)")
print()
print(f"{'published commits (K)':<26}{'stateless':<12}{'state-indexed'}")
for pub in [(), ("base",), ("c1",), ("c2",), ("c3",)]:
    s = make_state(pub)
    after, _ = apply(s, op)
    print(f"{str(set(pub) or '{}'):<26}{str(std_stateless(op, s, after)):<12}{std(s, op)}")

print()
print("A trace: assess the rewrite, publish c2 (a commitment transition), assess again.")
s0 = make_state()
s1 = dict(s0, published=s0["published"] | {"c2"})
print("  before publication:", std(s0, op))
print("  after publication: ", std(s1, op))
assert std(s0, op) is True and std(s1, op) is False
assert std_stateless(op, s1, apply(s1, op)[0]) is True

print()
print("Result: the stateless assessment returns the same verdict in every row, so it")
print("is wrong for at least one of s0 and s1. Standing attaches to the transition in")
print("a state, and a commitment transition changes what later transitions require.")

[The Conditions of Standing](https://standardgalactic.github.io/conditions-of-standing/conditions-of-standing.pdf)

Generation, Inscription, Evaluation, Authorization, and Commitment as Distinct Transitions.

This repository holds a short keystone document that consolidates an existing body of work around one question: what warrants treating a candidate, such as a claim, a proof, a policy or a change to a shared record, as entitled to count for a stated purpose. It borrows the word standing from law for its structure only and takes no position on legal doctrine. It does not announce a new theory and does not derive other frameworks from one theorem. It fixes a vocabulary, states five structural results with their assumptions, applies them to five cases, and says where they stop.

Admissibility is a related concept and is treated at length in *The Cost of Future Admissibility*, which is cited for commitment and reversibility and not restated.

## Contents

`main.tex` is the principal document, with its sections in `sec1.tex` to `sec5.tex`. The compiled `main.pdf` is 17 pages. `examples/` holds four short programs that reproduce selected claims, each with its expected output in `examples/expected/`. `MAP.md` relates the other essays in the corpus to the keystone, with a provisional primary category for each.

## Building and checking

The document builds with `latexmk -pdf main.tex`, or with `make pdf`. The examples need only Python 3 and the standard library. Running `examples/check.sh`, or `make check`, runs each program and compares its output with the saved expected output. The programs are deterministic; the self-distillation example uses fixed seeds.

## What each example shows

`ex1_ledgers.py` gives two records with the same number of inscriptions, observations and citation links and different sets of items with standing, and searches all records of four inscriptions to show that count-based summaries do not determine warranted content (Proposition 5). `ex2_branching.py` assesses one history rewrite, on the same evidence, in states that differ only in which commits are published, and shows that standing attaches to the transition in a state (Proposition 2, commitments). `ex3_selfdistillation.py` runs a self-distillation loop with known ground truth under five stated conditions, separating selection, training, evaluation that only measures, and evaluation that changes selection; its result holds under the stated conditions and is not claimed in general. `ex4_countermodels.py` searches small rule systems and small evidence models for the countermodels behind Propositions 1 and 2.

## Status

The repository is a first full draft. The corpus map is provisional and each assignment in it should be confirmed against the essay before publication. The technical references named in the map are deliberately kept outside this repository.

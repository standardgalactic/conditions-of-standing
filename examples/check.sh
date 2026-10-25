#!/bin/sh
# Runs each example and compares its output with the saved expected output.
cd "$(dirname "$0")" || exit 1
status=0
for f in ex1_ledgers ex2_branching ex3_selfdistillation ex4_countermodels; do
  if python3 -I "$f.py" | diff -q - "expected/$f.txt" >/dev/null; then
    echo "ok    $f"
  else
    echo "DIFF  $f"; status=1
  fi
done
exit $status

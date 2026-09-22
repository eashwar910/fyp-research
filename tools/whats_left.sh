#!/usr/bin/env bash
# tools/whats_left.sh — derive remaining stage-4 work from the filesystem, not from any list.
# See RUNBOOK.md §8. The filesystem is the state; ledgers are only an audit trail.
cd "$(git rev-parse --show-toplevel)"

# Free kills — resolved without a dispatch, so they must never appear as outstanding.
# R4-S20  : novelty already `closed` with evidence -> fail / C7      (RUNBOOK §1.2.3)
# R4-S124 : BCA TR78 thermal archive `blocked`     -> fail / C9      (RUNBOOK §3.2)
# R4-S131 : same precheck, same reason             -> fail / C9      (RUNBOOK §3.2)
# They also drop out of NV once fold-in routes them in gate_screen.yml; this list makes the
# script correct *before* that has happened too.
FREE_KILLS="R4-S20 R4-S124 R4-S131"

is_free_kill() {
  case " $FREE_KILLS " in *" $1 "*) return 0 ;; *) return 1 ;; esac
}

NV=$(awk '/^verify:/,/^verify_summary:/' .research/gate_screen.yml \
     | grep -B1 'route: not_verified' | grep -o 'R4-S[0-9]*')

echo "== novelty outstanding =="
for id in $NV; do
  is_free_kill "$id" && continue
  [ -f ".research/novelty/$id.json" ] || echo "  nov:$id"
done

echo "== data outstanding =="
for id in $NV; do
  is_free_kill "$id" && continue
  # R4-S47 has no data envelope by design: its data verdict is already `conditional`.
  [ "$id" = "R4-S47" ] && continue
  [ -f ".research/data/$id.json" ] || echo "  dat:$id"
done

echo "== deep re-dispatch (unclear) =="
for id in R4-S25 R4-S28 R4-S30; do
  grep -q "\"depth\": *\"deep\"" ".research/novelty/$id.json" 2>/dev/null || echo "  nov:$id (deep)"
done

echo "== free kills (no dispatch — route at fold-in) =="
for id in $FREE_KILLS; do
  grep -q "id: $id" .research/gate_screen.yml 2>/dev/null \
    && echo "  $id — confirm routed to fail in gate_screen.yml"
done

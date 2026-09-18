#!/usr/bin/env bash
# tools/whats_left.sh
cd "$(git rev-parse --show-toplevel)"
NV=$(awk '/^verify:/,/^verify_summary:/' .research/gate_screen.yml \
     | grep -B1 'route: not_verified' | grep -o 'R4-S[0-9]*')
echo "== novelty outstanding =="
for id in $NV; do
  [ "$id" = "R4-S20" ] && continue                      # free C7 kill, no dispatch
  [ -f ".research/novelty/$id.json" ] || echo "  nov:$id"
done
echo "== data outstanding =="
for id in $NV; do
  [ "$id" = "R4-S20" ] && continue
  [ -f ".research/data/$id.json" ] || echo "  dat:$id"
done
echo "== deep re-dispatch (unclear) =="
for id in R4-S25 R4-S28 R4-S30; do
  grep -q "\"depth\": *\"deep\"" ".research/novelty/$id.json" 2>/dev/null || echo "  nov:$id (deep)"
done

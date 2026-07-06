#!/usr/bin/env bash

set -euo pipefail
shopt -s nullglob

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="$ROOT_DIR/build/test_notebooks"

# Mode:
# "0": test all notebooks
# "1": test anything changed in the most recent commit
# "2": test anything uncommitted (including staged and unstaged)
MODE="${MODE:-0}"

# Timeout in seconds for each notebook execution.
# Use -1 to disable timeout.
EXECUTION_TIMEOUT="${EXECUTION_TIMEOUT:-7200}"

# Fail-fast behavior:
# "1": stop on first failing notebook (default)
# "0": continue running all notebooks and report all failures
FAIL_FAST="${FAIL_FAST:-1}"

mkdir -p "$OUT_DIR"

if ! command -v jupyter >/dev/null 2>&1; then
  echo "Error: jupyter command not found in PATH." >&2
  exit 2
fi

echo "Notebook test configuration"
echo "  ROOT_DIR:           $ROOT_DIR"
echo "  OUT_DIR:            $OUT_DIR"
echo "  MODE:               $MODE"
echo "  EXECUTION_TIMEOUT:  $EXECUTION_TIMEOUT"
echo "  FAIL_FAST:          $FAIL_FAST"

# Build list of changed files for git-based modes (paths relative to ROOT_DIR).
changed_files=""
if [[ "$MODE" == "1" ]]; then
  changed_files="$(git -C "$ROOT_DIR" diff-tree --no-commit-id -r --name-only HEAD 2>/dev/null)" || {
    echo "Error: could not read git history." >&2; exit 2
  }
elif [[ "$MODE" == "2" ]]; then
  changed_files="$({ git -C "$ROOT_DIR" diff --name-only HEAD; \
                      git -C "$ROOT_DIR" diff --cached --name-only HEAD; } 2>/dev/null | sort -u)" || {
    echo "Error: could not read git status." >&2; exit 2
  }
fi

total=0
passed=0
failed=0
declare -a failed_notebooks=()

start_ts="$(date +%s)"

for pack_dir in "$ROOT_DIR"/starter_pack_*; do
  [[ -d "$pack_dir" ]] || continue

  pack_name="$(basename "$pack_dir")"
  notebooks=("$pack_dir"/notebooks/*.ipynb)

  for nb in "${notebooks[@]}"; do
    [[ -f "$nb" ]] || continue

    # In git-based modes, skip notebooks not in the changed-files list.
    if [[ "$MODE" != "0" ]]; then
      nb_rel="${nb#"$ROOT_DIR"/}"
      grep -qF "$nb_rel" <<< "$changed_files" || continue
    fi

    total=$((total + 1))

    nb_base="$(basename "${nb%.*}")"
    out_nb="${pack_name}_${nb_base}.executed.ipynb"

    echo "[$total] Executing $nb"

    if jupyter nbconvert \
      --to notebook \
      --execute "$nb" \
      --ExecutePreprocessor.timeout="$EXECUTION_TIMEOUT" \
      --output "$out_nb" \
      --output-dir "$OUT_DIR"; then
      passed=$((passed + 1))
      echo "    OK"
    else
      failed=$((failed + 1))
      failed_notebooks+=("$nb")
      echo "    ERROR"

      if [[ "$FAIL_FAST" == "1" ]]; then
        echo "    Fail-fast enabled: stopping after first notebook failure."
        echo
        echo "Notebook execution summary"
        echo "  Total:  $total"
        echo "  Passed: $passed"
        echo "  Failed: $failed"
        echo "  Seconds: $(( $(date +%s) - start_ts ))"
        echo
        echo "Notebooks with errors:"
        echo "  - $nb"
        exit 1
      fi
    fi
  done
done

echo
echo "Notebook execution summary"
echo "  Total:  $total"
echo "  Passed: $passed"
echo "  Failed: $failed"
echo "  Seconds: $(( $(date +%s) - start_ts ))"

if (( failed > 0 )); then
  echo
  echo "Notebooks with errors:"
  for nb in "${failed_notebooks[@]}"; do
    echo "  - $nb"
  done
  exit 1
fi

exit 0

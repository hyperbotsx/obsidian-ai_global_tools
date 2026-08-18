#!/usr/bin/env bash
set -euo pipefail

role="${1:-}"
case "$role" in
  coder|verifier|researcher|git-manager|steward) ;;
  *)
    echo "usage: $(basename "$0") <coder|verifier|researcher|git-manager|steward> [--resume <session-file-or-id>]" >&2
    exit 2
    ;;
esac
shift

resume=()
if [[ "${1:-}" == "--resume" && -n "${2:-}" && $# -eq 2 ]]; then
  resume=(--session "$2")
elif [[ $# -ne 0 ]]; then
  echo "usage: $(basename "$0") <role> [--resume <session-file-or-id>]" >&2
  exit 2
fi

worktree_root="$(git rev-parse --show-toplevel)"
branch="$(git branch --show-current)"
if [[ -z "$branch" ]]; then
  echo "refusing to launch from a detached HEAD" >&2
  exit 3
fi

worktree_name="$(basename "$worktree_root")"
project="${PI_AGENT_COMS_PROJECT:-$worktree_name}"
expected_title="π - $role - $worktree_name"
matches=()
while IFS=$'\t' read -r session pane_cwd title; do
  if [[ "$pane_cwd" == "$worktree_root" && "$title" == "$expected_title" ]]; then
    matches+=("$session")
  fi
done < <(tmux list-panes -a -F '#{session_name}|#{pane_current_path}|#{pane_title}' 2>/dev/null | tr '|' '\t' || true)

if (( ${#matches[@]} == 1 )); then
  printf 'Reusing %s for %s in %s (%s).\n' "${matches[0]}" "$role" "$worktree_name" "$branch"
  printf 'Attach: tmux attach-session -t %s\n' "${matches[0]}"
  exit 0
fi
if (( ${#matches[@]} > 1 )); then
  printf 'Refusing to choose among duplicate %s panes in %s:\n' "$role" "$worktree_name" >&2
  printf '  %s\n' "${matches[@]}" >&2
  exit 4
fi

launcher="${PI_AGENT_LAUNCHER:-}"
if [[ -z "$launcher" && -x "$worktree_root/scripts/agentops/pi-agent.sh" ]]; then
  launcher="$worktree_root/scripts/agentops/pi-agent.sh"
fi
if [[ -z "$launcher" && -x "${AGENTOPS_HARNESS_ROOT:-/mnt/hyperliquid-data/projects/repos/agentops-harness}/scripts/agentops/pi-agent.sh" ]]; then
  launcher="${AGENTOPS_HARNESS_ROOT:-/mnt/hyperliquid-data/projects/repos/agentops-harness}/scripts/agentops/pi-agent.sh"
fi
if [[ -z "$launcher" || ! -x "$launcher" ]]; then
  echo "pi-agent launcher not found; set PI_AGENT_LAUNCHER to its executable path" >&2
  exit 5
fi

session="coms-${role}-${worktree_name}"
model="${PI_COMS_PANE_MODEL:-openai-codex/gpt-5.6-sol}"
thinking="${PI_COMS_PANE_THINKING:-max}"
label="${PI_COMS_MODEL_LABEL:-${model#*/}}"

tmux new-session -d -s "$session" -c "$worktree_root" -- \
  env PI_AGENT_COMS_MODE=harness-native PI_AGENT_COMS_PROJECT="$project" PI_COMS_MODEL_LABEL="$label" \
  "$launcher" "$role" --model "$model" --thinking "$thinking" "${resume[@]}"
sleep 1
if ! tmux has-session -t "$session" 2>/dev/null; then
  echo "Pi exited while starting $role; inspect the launch command or tmux server logs" >&2
  exit 6
fi

printf 'Started %s for %s in %s (%s).\n' "$session" "$role" "$worktree_name" "$branch"
printf 'Attach: tmux attach-session -t %s\n' "$session"

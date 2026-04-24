#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd -P)"
source "$REPO_ROOT/deploy/deployment-config.sh"

AGENT_WORKTREE_PARENT="${AGENT_WORKTREE_PARENT:-/mnt/hyperliquid-data/projects/worktrees/Evonome-agents}"

log() {
  printf '[workflow] %s\n' "$*"
}

fail() {
  log "ERROR: $*"
  exit 1
}

require_args() {
  [[ $# -gt 0 ]] || fail "Missing required arguments"
}

current_root() {
  git rev-parse --show-toplevel
}

current_branch() {
  git branch --show-current
}

require_clean_tree() {
  local root
  root="$(current_root)"
  git -C "$root" diff --quiet --ignore-submodules --exit-code -- || fail "Tracked working tree has unstaged changes"
  git -C "$root" diff --cached --quiet --ignore-submodules --exit-code -- || fail "Index has staged changes"
  [[ -z "$(git -C "$root" ls-files --others --exclude-standard)" ]] || fail "Working tree has untracked files"
}

require_shared_tree_clean() {
  git -C "$DEV_MAIN_ROOT" diff --quiet --ignore-submodules --exit-code -- || fail "$DEV_MAIN_ROOT has unstaged changes"
  git -C "$DEV_MAIN_ROOT" diff --cached --quiet --ignore-submodules --exit-code -- || fail "$DEV_MAIN_ROOT has staged changes"
  [[ -z "$(git -C "$DEV_MAIN_ROOT" ls-files --others --exclude-standard)" ]] || fail "$DEV_MAIN_ROOT has untracked files"
}

validate_branch_type() {
  case "$1" in
    feat|fix|chore|docs) ;;
    *) fail "Branch type must be one of: feat, fix, chore, docs" ;;
  esac
}

validate_slug() {
  [[ "$1" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail "Slug must be kebab-case"
}

validate_slice() {
  [[ "$1" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail "Slice must be kebab-case"
}

branch_exists() {
  git show-ref --verify --quiet "refs/heads/$1"
}

load_sprint_context() {
  local branch
  branch="$(current_branch)"
  [[ "$branch" =~ ^(feat|fix|chore|docs)/([a-z0-9]+(-[a-z0-9]+)*)$ ]] || fail "Current branch must be a sprint branch"
  SPRINT_BRANCH="$branch"
  SPRINT_TYPE="${BASH_REMATCH[1]}"
  SPRINT_SLUG="${BASH_REMATCH[2]}"
}

agent_branch_name() {
  printf 'agent/%s/%s\n' "$SPRINT_SLUG" "$1"
}

agent_worktree_path() {
  printf '%s/%s-%s\n' "$AGENT_WORKTREE_PARENT" "$SPRINT_SLUG" "$1"
}

sync_shared_dev_main() {
  log "Syncing $DEV_MAIN_BRANCH from origin/main in $DEV_MAIN_ROOT"
  git -C "$DEV_MAIN_ROOT" fetch origin main
  git -C "$DEV_MAIN_ROOT" branch -f "$DEV_MAIN_BRANCH" origin/main
  git -C "$DEV_MAIN_ROOT" switch "$DEV_MAIN_BRANCH"
}

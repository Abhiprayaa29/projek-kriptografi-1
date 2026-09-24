#!/usr/bin/env bash
# Auto-commit + auto-push + auto-pull setiap ada perubahan di folder ini.
# Dijalankan oleh systemd user service: autosync-projek-kriptografi.service
set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_FILE="$REPO_DIR/.autosync.lock"
LOG_FILE="$REPO_DIR/.autosync.log"
INTERVAL_SEC=2
SETTLE_SEC=1

# Rate-limit log galat: hanya saat pesan berubah atau tiap ~30 kegagalan.
LAST_PULL_ERR=""
LAST_PUSH_ERR=""
PULL_FAIL_N=0
PUSH_FAIL_N=0

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG_FILE"
}

log_fail() {
  # $1=kind $2=err $3=last_msg_var $4=counter_var — update variabel global via eval.
  local kind="$1" err="$2" last_name="$3" count_name="$4"
  local n short prev
  n=$(( ${!count_name:-0} + 1 ))
  short="$(printf '%s' "$err" | head -n 3 | tr '\n' '|' | cut -c1-400)"
  [[ -z "$short" ]] && short="galat tidak diketahui"
  prev="${!last_name:-}"
  if [[ "$n" -eq 1 || "$short" != "$prev" || $((n % 30)) -eq 0 ]]; then
    log "$kind FAIL (x$n): $short"
    eval "$last_name=\$short"
  fi
  eval "$count_name=\$n"
}

sync_once() {
  exec 9>"$LOCK_FILE"
  if ! flock -n 9; then
    return 0
  fi

  cd "$REPO_DIR" || return 1

  local dirty=0
  local changed=""
  if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
    sleep "$SETTLE_SEC"
    if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
      dirty=1
      changed="$(git status --porcelain | head -20 | tr '\n' '; ')"
      git add -A || true
      git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S') [$(git config user.name || echo unknown)]" >/dev/null 2>&1 || true
    fi
  fi

  local before after push_ok=1 pull_err="" push_err=""
  before="$(git rev-parse HEAD 2>/dev/null || true)"

  if ! pull_err="$(git pull --rebase --autostash 2>&1)"; then
    log_fail PULL "$pull_err" LAST_PULL_ERR PULL_FAIL_N
  else
    PULL_FAIL_N=0
    LAST_PULL_ERR=""
  fi

  if ! push_err="$(git push 2>&1)"; then
    push_ok=0
    log_fail PUSH "$push_err" LAST_PUSH_ERR PUSH_FAIL_N
  else
    PUSH_FAIL_N=0
    LAST_PUSH_ERR=""
  fi

  after="$(git rev-parse HEAD 2>/dev/null || true)"

  if [[ "$dirty" -eq 1 ]]; then
    if [[ "$push_ok" -eq 1 ]]; then
      log "PUSHED: $changed"
    else
      log "COMMIT_OK_PUSH_FAIL: $changed"
    fi
  elif [[ -n "$before" && -n "$after" && "$before" != "$after" ]]; then
    log "PULLED: update dari GitHub"
  fi

  flock -u 9
}

log "watcher started (pid $$)"

while true; do
  sync_once
  sleep "$INTERVAL_SEC"
done

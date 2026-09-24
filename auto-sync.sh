#!/usr/bin/env bash
# Auto-commit + auto-push + auto-pull setiap ada perubahan di folder ini.
# Dijalankan oleh systemd user service: autosync-projek-kriptografi.service
set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_FILE="$REPO_DIR/.autosync.lock"
LOG_FILE="$REPO_DIR/.autosync.log"
INTERVAL_SEC=2
SETTLE_SEC=1

log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG_FILE"
}

sync_once() {
  # Jangan jalankan dua proses sync bersamaan.
  exec 9>"$LOCK_FILE"
  if ! flock -n 9; then
    return 0
  fi

  cd "$REPO_DIR" || return 1

  local dirty=0
  local changed=""
  if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
    # Tunggu sebentar supaya file yang sedang disimpan selesai ditulis.
    sleep "$SETTLE_SEC"
    if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
      dirty=1
      changed="$(git status --porcelain | head -20 | tr '\n' '; ')"
      git add -A || true
      git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S') [$(git config user.name || echo unknown)]" >/dev/null 2>&1 || true
    fi
  fi

  local before after push_ok=1
  before="$(git rev-parse HEAD 2>/dev/null || true)"
  git pull --rebase --autostash >/dev/null 2>&1 || true
  if ! git push >/dev/null 2>&1; then
    push_ok=0
  fi
  after="$(git rev-parse HEAD 2>/dev/null || true)"

  if [[ "$dirty" -eq 1 ]]; then
    if [[ "$push_ok" -eq 1 ]]; then
      log "PUSHED: $changed"
    else
      log "COMMIT_OK_PUSH_FAIL (offline / conflict?): $changed"
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

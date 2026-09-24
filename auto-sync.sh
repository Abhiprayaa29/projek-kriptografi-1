#!/usr/bin/env bash
# Auto-commit + auto-push setiap ada perubahan file di folder ini.
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

  if [[ -z "$(git status --porcelain 2>/dev/null)" ]]; then
    return 0
  fi

  # Tunggu sebentar supaya file yang sedang disimpan selesai ditulis.
  sleep "$SETTLE_SEC"
  if [[ -z "$(git status --porcelain 2>/dev/null)" ]]; then
    return 0
  fi

  local changed
  changed="$(git status --porcelain | head -20 | tr '\n' '; ')"

  if git add -A; then
    if git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S') [$(git config user.name || echo unknown)]" >/dev/null 2>&1; then
      if git push >/dev/null 2>&1; then
        log "PUSHED: $changed"
      elif git pull --rebase --autostash >/dev/null 2>&1 && git push >/dev/null 2>&1; then
        log "PUSHED_AFTER_REBASE: $changed"
      else
        log "COMMIT_OK_PUSH_FAIL (offline / conflict?): $changed"
      fi
    fi
  else
    log "COMMIT_FAIL: $changed"
  fi

  flock -u 9
}

log "watcher started (pid $$)"

while true; do
  sync_once
  sleep "$INTERVAL_SEC"
done

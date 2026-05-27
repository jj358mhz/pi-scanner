#!/bin/bash

LAST_IP=""

while true; do
  CUR_IP=$(curl -s --max-time 5 https://api.ipify.org)
  if [ -n "$CUR_IP" ] && [ -n "$LAST_IP" ] && [ "$CUR_IP" != "$LAST_IP" ]; then
    logger -t darkice-watchdog "WAN IP changed: $LAST_IP -> $CUR_IP, restarting darkice"
    nohup systemd-run --no-block systemctl restart darkice >/dev/null 2>&1
  fi
  [ -n "$CUR_IP" ] && LAST_IP="$CUR_IP"
  sleep 10
done

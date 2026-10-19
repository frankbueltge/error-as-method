#!/bin/sh
# keep.sh <maker> <round>: saves the hand-back of that round, keeps the version it left, logs the next K send.
cd "$(dirname "$0")"
python3 savereport.py "$1" "$2" && python3 snap.py "$1" "$2" | cut -c1-170
[ "$2" -lt 6 ] && echo "{\"maker\":\"$1\",\"round\":$(($2+1)),\"sent\":\"again-K.md\",\"time\":\"$(date -u +%FT%TZ)\"}" >> sends.jsonl
true

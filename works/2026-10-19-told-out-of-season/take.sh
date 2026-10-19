#!/bin/sh
# take.sh <maker>: saves the maker's report from its transcript and collects its work folder.
cd "$(dirname "$0")"
id=$(python3 -c "import json,sys;print(json.load(open('agents.json'))[sys.argv[1]])" "$1")
python3 savereport.py "$1" /tmp/claude-0/-home-user/7fc18ae2-2ba2-52d2-ab4b-d859cd46d88d/tasks/$id.output && python3 collect.py "$1"

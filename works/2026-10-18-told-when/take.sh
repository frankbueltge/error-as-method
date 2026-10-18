#!/bin/sh
# take.sh <maker>: saves the maker's report from its transcript and collects its work folder.
cd "$(dirname "$0")"
id=$(python3 -c "import json,sys;print(json.load(open('agents.json'))[sys.argv[1]])" "$1")
python3 savereport.py "$1" /tmp/claude-0/-home-user/eec7a316-5b88-57f9-b44e-a97806d15d1b/tasks/$id.output && python3 collect.py "$1"

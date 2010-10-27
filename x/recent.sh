find  -type f -mtime -$1 | grep -v '\.git\|~\|\.pyc'

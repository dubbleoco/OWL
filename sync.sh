#!/bin/bash
cd /Users/dubbleo/OWL

# Export pellets
/opt/homebrew/bin/python3 /Users/dubbleo/OWL/export.py

# Push to GitHub if changed
if ! /usr/bin/git diff --quiet pellets.json 2>/dev/null; then
    /usr/bin/git add pellets.json
    /usr/bin/git commit -m "sync pellets" --quiet
    /usr/bin/git push --quiet
fi

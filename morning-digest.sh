#!/bin/bash
cd /Users/dubbleo/OWL

# Sync pellets first
/Users/dubbleo/OWL/sync.sh

# Send email digest
/opt/homebrew/bin/python3 /Users/dubbleo/OWL/send-digest.py

# Send iMessage link
osascript -e 'tell application "Messages" to send "🦉 Your Owl digest is ready: https://dubbleoco.github.io/OWL/swipe.html" to buddy "+17343303842" of (service 1 whose service type is iMessage)'

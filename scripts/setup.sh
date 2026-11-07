#!/usr/bin/env bash
echo "Setting up MARK 12..."
python3 -m pip install -r requirements.txt
python3 database/init_db.py
python3 scripts/create_admin.py admin jarvis2026
echo "Setup complete."

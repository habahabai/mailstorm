#!/bin/bash
echo "Installing PyInstaller if not already installed..."
pip install pyinstaller

echo "Running PyInstaller..."
pyinstaller --onefile \
  --add-data "tor:tor" \
  main.py

echo "Build complete. Check the 'dist' folder for the executable."

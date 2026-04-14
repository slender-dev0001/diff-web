@echo off
title DIFF Web Config
echo [*] Installation des dependances web...
pip install -r requirements.txt
echo [*] Lancement de l interface locale...
python DIFF-tool.py
pause

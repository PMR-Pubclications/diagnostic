# ==========================================
# DIAGNOSTIC CORE MAKEFILE
# ==========================================

.PHONY: help diagnose hardware voice clean

help:
	@echo "----------------------------------------"
	@echo " DIAGNOSTIC CORE - COMMAND REFERENCE    "
	@echo "----------------------------------------"
	@echo "  make diagnose   - Run full multi-repo health scan"
	@echo "  make hardware   - Check C++ engine hardware stream status"
	@echo "  make voice      - Run voice controller test sequence"
	@echo "  make clean      - Remove Python cache files"
	@echo "----------------------------------------"

diagnose:
	@echo "Running multi-repository diagnostic scan..."
	python3 scripts/utils/repo_inspector.py

hardware:
	@echo "Executing C++ hardware engine check..."
	python3 -c "from scripts.voice.voice_controller import AudioVideoVoiceBridge; bridge = AudioVideoVoiceBridge(); print(bridge.execute_engine_command(['--status']))"

voice:
	@echo "Launching Voice Controller interface..."
	python3 scripts/voice/voice_controller.py

clean:
	@echo "Cleaning up local cache files..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	@echo "Cleanup complete."

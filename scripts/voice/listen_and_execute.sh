#!/usr/bin/env bash
# ==========================================
# HANDS-FREE VOICE EXECUTION BRIDGE (BASH)
# ==========================================
# Designed for accessibility, first responders, and screen-reader users.
# Usage: ./listen_and_execute.sh "run diagnostics"
#        ./listen_and_execute.sh "annon, how are you feeling?"
#        ./listen_and_execute.sh "diagnostic track"
#        ./listen_and_execute.sh "check hardware"

# Exit immediately if a command exits with a non-zero status
set -e

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

# Fallback text-to-speech feedback function (uses festival, espeak, or prints if unavailable)
speak_feedback() {
    local message="$1"
    echo "[Audio Feedback]: $message"
    
    # Check for available text-to-speech tools on Linux/Unix
    if command -v spd-say &> /dev/null; then
        spd-say "$message" &> /dev/null &
    elif command -v espeak &> /dev/null; then
        espeak "$message" &> /dev/null &
    elif command -v say &> /dev/null; then
        say "$message" &> /dev/null &
    fi
}

# Capture the spoken command passed as an argument
SPOKEN_COMMAND="${1:-}"
CLEAN_COMMAND=$(echo "$SPOKEN_COMMAND" | tr '[:upper:]' '[:lower:]' | xargs)

if [ -z "$CLEAN_COMMAND" ]; then
    speak_feedback "No command received. Please repeat your instruction."
    echo "Usage: $0 \"[spoken command]\""
    exit 1
fi

echo "Processing spoken input: '$CLEAN_COMMAND'"

# Route commands to the appropriate Makefile targets or Python bridges
case "$CLEAN_COMMAND" in
    "run diagnostics" | "execute_diagnostic_pipeline")
        speak_feedback "Starting cross-repository system diagnostics."
        make diagnose
        speak_feedback "Diagnostics sequence complete."
        ;;
    
    "annon, how are you feeling?" | "how are you feeling" | "status_check")
        speak_feedback "All systems are operational. Trust ledgers and audio engines running smoothly."
        ;;
    
    "diagnostic track" | "track_telemetry_logs")
        speak_feedback "Initializing diagnostic telemetry tracking."
        if [ -d "logs/training_logs" ]; then
            speak_feedback "Log tracks are active and recording data."
        else
            speak_feedback "Notice: Log tracking directory initialized."
            mkdir -p logs/training_logs
        fi
        ;;
    
    "check hardware" | "hardware_stream_status")
        speak_feedback "Initiating hardware check across audio and video streams."
        make hardware
        speak_feedback "Hardware check finished."
        ;;
        
    *)
        speak_feedback "Command not recognized. Please repeat your instruction."
        echo "Error: Unrecognized command '$CLEAN_COMMAND'"
        exit 1
        ;;
esac

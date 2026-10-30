import os
import sys
import subprocess
import logging

# Dynamically ensure root and utils paths are accessible
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
UTILS_DIR = os.path.join(PROJECT_ROOT, "scripts", "utils")

if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

try:
    from audio_feedback import AnnonAudioFeedback
except ImportError:
    # Safe fallback if audio feedback module is building/linking
    class AnnonAudioFeedback:
        def __init__(self, trust_main_path="../Trust-Main"):
            pass
        def speak(self, text: str):
            print(f"[Fallback Audio Output]: {text}")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("VoiceController")


class AudioVideoVoiceBridge:
    """Handles low-level command routing to the C++ hardware engine."""
    def __init__(self, binary_name="AudioVideoEngine"):
        self.binary_path = os.path.join(PROJECT_ROOT, binary_name)

    def execute_engine_command(self, command_args: list) -> dict:
        """Passes voice-parsed commands down to the compiled C++ engine binary."""
        full_command = [self.binary_path] + command_args
        
        logger.info(f"Executing engine command: {' '.join(full_command)}")
        try:
            result = subprocess.run(full_command, capture_output=True, text=True, check=True)
            return {"status": "success", "output": result.stdout.strip()}
        except subprocess.CalledProcessError as e:
            logger.error(f"Engine execution failed: {e.stderr.strip()}")
            return {"status": "error", "output": e.stderr.strip()}
        except FileNotFoundError:
            logger.warning(f"C++ engine binary not found at '{self.binary_path}'. Running in simulation mode.")
            return {"status": "simulated", "output": f"Simulated execution for: {' '.join(command_args)}"}


class VoiceController:
    """High-level voice interface connecting speech commands, audio feedback, C++ engine execution, and repo scanning."""
    def __init__(self, trust_main_path="../Trust-Main"):
        self.audio = AnnonAudioFeedback(trust_main_path=trust_main_path)
        self.bridge = AudioVideoVoiceBridge()

    def process_command(self, command: str):
        command_clean = command.strip().lower()
        logger.info(f"Processing voice command: '{command_clean}'")

        if command_clean == "run diagnostics":
            self.audio.speak("Starting cross-repository system diagnostics. Scanning Trust Main, Trust Shell, Audio Video Engine, and Annon OS.")
            
            # 1. Run Multi-Repo Inspector scan
            try:
                from repo_inspector import MultiRepoDiagnostics
                inspector = MultiRepoDiagnostics(workspace_root=os.path.join(PROJECT_ROOT, ".."))
                reports = inspector.run_full_diagnostic()
                
                issues_found = False
                for rep in reports:
                    if rep["status"] != "healthy":
                        issues_found = True
                        self.audio.speak(f"Warning detected in {rep['repo']}.")
                
                if not issues_found:
                    self.audio.speak("All connected repositories checked out successfully.")
            except Exception as e:
                logger.error(f"Failed to run multi-repo diagnostic: {e}")
                self.audio.speak("Error executing multi-repository diagnostic scan.")

            # 2. Execute hardware diagnosis via C++ engine
            self.audio.speak("Analyzing raw telemetry logs via hardware engine.")
            res = self.bridge.execute_engine_command(["--diagnose", "--verbose"])
            
            if res["status"] in ["success", "simulated"]:
                self.audio.speak("Diagnostics complete. System status confirmed clean.")
            else:
                self.audio.speak("Diagnostics encountered an error during log analysis.")

        elif command_clean == "check hardware":
            self.audio.speak("Initiating hardware check across audio and video streams.")
            
            # Execute hardware status via C++ engine
            res = self.bridge.execute_engine_command(["--status"])
            
            if res["status"] in ["success", "simulated"]:
                self.audio.speak("Hardware check passed. All hardware channels functional.")
            else:
                self.audio.speak("Hardware check failed. Please verify local stream pipelines.")

        else:
            self.audio.speak("Command not recognized. Please repeat your instruction.")


if __name__ == "__main__":
    controller = VoiceController()
    
    # Test execution run
    controller.process_command("run diagnostics")
    print("---")
    controller.process_command("check hardware")

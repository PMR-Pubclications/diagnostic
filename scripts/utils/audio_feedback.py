import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DiagnosticAudioFeedback")

class AnnonAudioFeedback:
    def __init__(self, trust_main_path="../Trust-Main"):
        """
        Locates the generate_annon_audio.py script within the Trust-Main repository.
        """
        self.trust_main_path = os.path.abspath(trust_main_path)
        self.script_path = os.path.join(
            self.trust_main_path, 
            "modules", "Annon", "audio", "generate_annon_audio.py"
        )
        
        if not os.path.exists(self.script_path):
            logger.warning(f"Audio script not found at expected path: {self.script_path}")

    def speak(self, message: str):
        """
        Triggers Annon's audio generation to speak diagnostic updates.
        """
        logger.info(f"[Annon Audio]: \"{message}\"")
        
        if not os.path.exists(self.script_path):
            logger.error("Cannot play audio: generate_annon_audio.py path invalid.")
            return False

        try:
            # Executes the audio script with the text message payload
            result = subprocess.run(
                [sys.executable, self.script_path, "--text", message],
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to generate audio feedback: {e.stderr.strip()}")
            return False

if __name__ == "__main__":
    # Test local audio feedback call
    speaker = AnnonAudioFeedback()
    speaker.speak("Diagnostic repository initialized and listening for voice commands.")

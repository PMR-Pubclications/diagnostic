import os
import hmac
import hashlib
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RepoHandshake")

class RepositoryHandshake:
    def __init__(self, shared_secret_env="REPO_SHARED_SECRET"):
        # Load a shared secret from the local environment for air-gapped security
        self.secret = os.environ.get(shared_secret_env, "default_local_diagnostic_secret_key").encode('utf-8')
        
    def generate_handshake_token(self, repo_name: str) -> dict:
        """Generates a signed challenge token for a target repository."""
        timestamp = str(int(time.time()))
        message = f"{repo_name}:{timestamp}".encode('utf-8')
        
        signature = hmac.new(self.secret, message, hashlib.sha256).hexdigest()
        
        token_payload = {
            "source_repo": repo_name,
            "timestamp": timestamp,
            "signature": signature
        }
        logger.info(f"Generated secure handshake token for: {repo_name}")
        return token_payload

    def verify_handshake(self, token_payload: dict, max_age_seconds: int = 300) -> bool:
        """Validates an incoming handshake token from one of the connected repositories."""
        try:
            repo_name = token_payload["source_repo"]
            timestamp = token_payload["timestamp"]
            received_signature = token_payload["signature"]
            
            # Check token expiration to prevent replay attacks
            current_time = int(time.time())
            if current_time - int(timestamp) > max_age_seconds:
                logger.warning(f"Handshake failed: Token from {repo_name} has expired.")
                return False
                
            # Recompute signature
            message = f"{repo_name}:{timestamp}".encode('utf-8')
            expected_signature = hmac.new(self.secret, message, hashlib.sha256).hexdigest()
            
            # Constant-time comparison to prevent timing attacks
            if hmac.compare_digest(expected_signature, received_signature):
                logger.info(f"Handshake successful with repository: {repo_name}")
                return True
            else:
                logger.error(f"Handshake failed: Signature mismatch for {repo_name}")
                return False
                
        except KeyError as e:
            logger.error(f"Handshake failed: Malformed token payload missing key {e}")
            return False

if __name__ == "__main__":
    # Test local handshake loop
    hs = RepositoryHandshake()
    
    # Simulate a handshake request from 'Trust-Main'
    token = hs.generate_handshake_token("Trust-Main")
    
    # Simulate verification on the diagnostic side
    is_valid = hs.verify_handshake(token)
    print(f"Handshake Verification Status: {is_valid}")

import os
import subprocess
import logging
import sys

# Ensure utils path is accessible
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RepoInspector")

class MultiRepoDiagnostics:
    def __init__(self, workspace_root="../"):
        """
        Initializes the inspector assuming the 4 repos are sibling directories 
        to the diagnostic project workspace.
        """
        self.workspace_root = os.path.abspath(workspace_root)
        self.target_repos = {
            "Trust-Main": os.path.join(self.workspace_root, "Trust-Main"),
            "Trust-Shell": os.path.join(self.workspace_root, "Trust-Shell"),
            "AudioVideoEngine-CPP": os.path.join(self.workspace_root, "AudioVideoEngine-CPP"),
            "AnnonOS": os.path.join(self.workspace_root, "AnnonOS")
        }

    def inspect_repository(self, repo_name: str, repo_path: str) -> dict:
        """Performs structural and test health checks on a specific repository."""
        logger.info(f"Inspecting repository: {repo_name} at {repo_path}")
        
        if not os.path.exists(repo_path):
            logger.error(f"Repository path not found: {repo_path}")
            return {"repo": repo_name, "status": "missing", "error": "Directory does not exist"}

        report = {"repo": repo_name, "status": "healthy", "issues": []}

        # 1. Check for common build or config files
        if repo_name == "AudioVideoEngine-CPP":
            build_dir = os.path.join(repo_path, "build")
            if not os.path.exists(build_dir):
                report["issues"].append("Missing CMake 'build' directory. Binary may need compilation.")
        
        # 2. Run unit tests if a test suite exists (e.g., pytest or make test)
        pytest_path = os.path.join(repo_path, "tests")
        if os.path.exists(pytest_path):
            try:
                test_result = subprocess.run(
                    ["pytest", pytest_path], 
                    capture_output=True, text=True, cwd=repo_path, timeout=30
                )
                if test_result.returncode != 0:
                    report["status"] = "test_failure"
                    report["issues"].append(f"Unit tests failed: {test_result.stderr.strip()[:200]}")
            except Exception as e:
                report["issues"].append(f"Could not execute test suite: {str(e)}")
        else:
            report["issues"].append("No 'tests/' directory detected.")

        if report["issues"]:
            report["status"] = "warning" if report["status"] == "healthy" else report["status"]

        return report

    def run_full_diagnostic(self) -> list:
        """Scans all four connected repositories and returns collective health reports."""
        results = []
        for name, path in self.target_repos.items():
            result = self.inspect_repository(name, path)
            results.append(result)
        return results

if __name__ == "__main__":
    inspector = MultiRepoDiagnostics()
    health_reports = inspector.run_full_diagnostic()
    
    print("\n=== MULTI-REPOSITORY DIAGNOSTIC REPORT ===")
    for rep in health_reports:
        print(f"[{rep['repo'].upper()}] Status: {rep['status'].upper()}")
        for issue in rep['issues']:
            print(f"  - {issue}")
    print("==========================================")

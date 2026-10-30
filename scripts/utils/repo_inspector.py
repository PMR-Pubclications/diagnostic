import os
import subprocess
import logging
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RepoInspector")

class MultiRepoDiagnostics:
    """Portable multi-repository scanner that reads paths dynamically from config."""
    def __init__(self, config_path=None):
        if not config_path:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.abspath(os.path.join(script_dir, "..", "..", "config", "config.yaml"))
        
        self.config = self._load_config(config_path)
        self.workspace_root = self._resolve_workspace_root()
        self.target_repos = self._resolve_repository_paths()

    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Could not load config file at {path}: {e}")
        
        # Fallback default configuration if yaml is missing
        return {
            "target_repositories": [
                {"name": "Trust-Main", "relative_path": "Trust-Main"},
                {"name": "Trust-Shell", "relative_path": "Trust-Shell"},
                {"name": "AudioVideoEngine-CPP", "relative_path": "AudioVideoEngine-CPP"},
                {"name": "AnnonOS", "relative_path": "AnnonOS"}
            ]
        }

    def _resolve_workspace_root(self) -> str:
        # Check environment variable override first, then fallback to relative offset
        workspace_cfg = self.config.get("workspace", {})
        env_var = workspace_cfg.get("env_override", "WORKSPACE_ROOT")
        default_offset = workspace_cfg.get("default_root_offset", "..")
        
        if os.environ.get(env_var):
            root = os.environ.get(env_var)
            logger.info(f"Using workspace root from environment variable '{env_var}': {root}")
            return os.path.abspath(root)
        
        # Fallback relative to diagnostic repo root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resolved = os.path.abspath(os.path.join(script_dir, "..", "..", default_offset))
        logger.info(f"Using resolved workspace root: {resolved}")
        return resolved

    def _resolve_repository_paths(self) -> dict:
        repos = {}
        repo_list = self.config.get("target_repositories", [])
        for repo in repo_list:
            name = repo.get("name")
            rel_path = repo.get("relative_path")
            repos[name] = os.path.join(self.workspace_root, rel_path)
        return repos

    def inspect_repository(self, repo_name: str, repo_path: str) -> dict:
        """Performs structural and test health checks on a specific repository."""
        logger.info(f"Inspecting repository: {repo_name} at {repo_path}")
        
        if not os.path.exists(repo_path):
            logger.error(f"Repository path not found: {repo_path}")
            return {"repo": repo_name, "status": "missing", "error": "Directory does not exist"}

        report = {"repo": repo_name, "status": "healthy", "issues": []}

        # Check for C++ build directory if applicable
        if repo_name == "AudioVideoEngine-CPP":
            build_dir = os.path.join(repo_path, "build")
            if not os.path.exists(build_dir):
                report["issues"].append("Missing CMake 'build' directory. Binary may need compilation.")
        
        # Run unit tests if a test suite exists
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
        """Scans all configured repositories and returns collective health reports."""
        results = []
        for name, path in self.target_repos.items():
            result = self.inspect_repository(name, path)
            results.append(result)
        return results

if __name__ == "__main__":
    inspector = MultiRepoDiagnostics()
    health_reports = inspector.run_full_diagnostic()
    
    print("\n=== PORTABLE MULTI-REPOSITORY DIAGNOSTIC REPORT ===")
    for rep in health_reports:
        print(f"[{rep['repo'].upper()}] Status: {rep['status'].upper()}")
        for issue in rep['issues']:
            print(f"  - {issue}")
    print("===================================================")

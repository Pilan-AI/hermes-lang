"""
Test all example .herm files to ensure they run without errors
"""
import subprocess
import sys
from pathlib import Path

# Path to examples directory
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
HERMES_MODULE = "hermes"

def run_hermes_file(filepath):
    """Run a .herm file and return (success, output, error)"""
    result = subprocess.run(
        [sys.executable, "-m", HERMES_MODULE, "run", str(filepath)],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.returncode == 0, result.stdout, result.stderr

def test_hello():
    """Test hello.herm example"""
    success, stdout, stderr = run_hermes_file(EXAMPLES_DIR / "hello.herm")
    assert success, f"hello.herm failed: {stderr}"
    assert "Hello, World!" in stdout
    assert "Greeting successful!" in stdout

def test_classes():
    """Test classes.herm example"""
    success, stdout, stderr = run_hermes_file(EXAMPLES_DIR / "classes.herm")
    assert success, f"classes.herm failed: {stderr}"
    assert "Hello, I am Raghu" in stdout
    assert "Raghu is now" in stdout

def test_fibonacci():
    """Test fibonacci.herm example"""
    success, stdout, stderr = run_hermes_file(EXAMPLES_DIR / "fibonacci.herm")
    assert success, f"fibonacci.herm failed: {stderr}"
    # Fibonacci sequence should be present
    assert "0" in stdout
    assert "1" in stdout

def test_api_server():
    """Test api_server.herm example"""
    success, stdout, stderr = run_hermes_file(EXAMPLES_DIR / "api_server.herm")
    assert success, f"api_server.herm failed: {stderr}"
    assert "HERMES CRUD" in stdout
    assert "Created user ID:" in stdout
    assert "Raghu" in stdout
    assert "Rocky Bhai" in stdout
    assert "Plan panni pannanum!" in stdout

if __name__ == "__main__":
    # Simple test runner
    tests = [test_hello, test_classes, test_fibonacci, test_api_server]
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  {test.__name__}: {e}")
            failed += 1
    
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(0 if failed == 0 else 1)

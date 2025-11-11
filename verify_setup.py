#!/usr/bin/env python3
"""
verify_setup.py
Verifies that the SCIRAG production structure is set up correctly
"""

import os
import sys
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check_exists(path, item_type="file"):
    """Check if a path exists"""
    p = Path(path)
    if p.exists():
        print(f"{GREEN}✓{RESET} {item_type.capitalize()}: {path}")
        return True
    else:
        print(f"{RED}✗{RESET} {item_type.capitalize()} missing: {path}")
        return False

def check_directory_structure():
    """Verify all required directories exist"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Checking Directory Structure{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    required_dirs = [
        "backend",
        "backend/app",
        "backend/app/agents",
        "backend/app/api",
        "backend/app/api/routes",
        "backend/app/models",
        "backend/app/services",
        "backend/app/tests",
        "backend/scripts",
        "docs",
        "frontend",
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if not check_exists(dir_path, "directory"):
            all_exist = False
    
    return all_exist

def check_init_files():
    """Verify all __init__.py files exist"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Checking __init__.py Files{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    required_inits = [
        "backend/app/__init__.py",
        "backend/app/agents/__init__.py",
        "backend/app/api/__init__.py",
        "backend/app/api/routes/__init__.py",
        "backend/app/models/__init__.py",
        "backend/app/services/__init__.py",
        "backend/app/tests/__init__.py",
    ]
    
    all_exist = True
    for init_file in required_inits:
        if not check_exists(init_file):
            all_exist = False
    
    return all_exist

def check_poc_files():
    """Verify POC files are in correct locations"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Checking POC Files{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    required_files = [
        "backend/requirements.txt",
        "backend/.env.example",
        "backend/scripts/scirag_poc.py",
        "backend/scripts/scirag_interactive.py",
        "backend/app/tests/test_scirag.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if not check_exists(file_path):
            all_exist = False
    
    return all_exist

def check_documentation():
    """Verify documentation files exist"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Checking Documentation{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    doc_files = [
        "docs/README.md",
        "docs/USAGE.md",
        "docs/ROADMAP.md",
        "docs/PROJECT_STRUCTURE.md",
        "docs/FILE_PLACEMENT_GUIDE.md",
        "docs/QUICK_REFERENCE.md",
    ]
    
    all_exist = True
    for doc_file in doc_files:
        if not check_exists(doc_file):
            all_exist = False
    
    return all_exist

def check_gitignore():
    """Verify .gitignore exists"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Checking Git Configuration{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    return check_exists(".gitignore")

def check_virtual_environment():
    """Check if virtual environment exists"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Checking Virtual Environment{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    venv_exists = check_exists("backend/venv", "directory")
    
    if not venv_exists:
        print(f"{YELLOW}ℹ{RESET}  Virtual environment not found.")
        print(f"{YELLOW}   Create it with: cd backend && python -m venv venv{RESET}")
    
    return venv_exists

def check_environment_variables():
    """Check if .env file exists"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Checking Environment Configuration{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    env_example_exists = check_exists("backend/.env.example")
    env_exists = check_exists("backend/.env")
    
    if env_example_exists and not env_exists:
        print(f"{YELLOW}ℹ{RESET}  .env file not found (this is normal if you haven't set it up yet)")
        print(f"{YELLOW}   Create it with: cp backend/.env.example backend/.env{RESET}")
        print(f"{YELLOW}   Then add your ANTHROPIC_API_KEY{RESET}")
    
    return env_example_exists

def check_poc_imports():
    """Check if POC scripts can be imported (basic syntax check)"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Checking POC Scripts (Syntax){RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    scripts_to_check = [
        "backend/scripts/scirag_poc.py",
        "backend/scripts/scirag_interactive.py",
    ]
    
    all_valid = True
    for script in scripts_to_check:
        if os.path.exists(script):
            try:
                with open(script, 'r') as f:
                    compile(f.read(), script, 'exec')
                print(f"{GREEN}✓{RESET} Valid Python syntax: {script}")
            except SyntaxError as e:
                print(f"{RED}✗{RESET} Syntax error in {script}: {e}")
                all_valid = False
        else:
            print(f"{YELLOW}⊘{RESET} File not found: {script}")
            all_valid = False
    
    return all_valid

def print_summary(results):
    """Print summary of all checks"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    total = len(results)
    passed = sum(results.values())
    
    if passed == total:
        print(f"{GREEN}✓ All checks passed! ({passed}/{total}){RESET}")
        print(f"{GREEN}  Your SCIRAG structure is set up correctly.{RESET}\n")
        print("Next steps:")
        print("1. cd backend")
        print("2. source venv/bin/activate  (or venv\\Scripts\\activate on Windows)")
        print("3. pip install -r requirements.txt")
        print("4. export ANTHROPIC_API_KEY='your-key'")
        print("5. python scripts/scirag_poc.py")
    else:
        print(f"{RED}✗ {total - passed} check(s) failed ({passed}/{total} passed){RESET}")
        print(f"{YELLOW}  Review the output above to see what's missing.{RESET}\n")
        print("Run the setup script:")
        print("  bash setup_structure.sh  (Linux/Mac)")
        print("  setup_structure.bat  (Windows)")

def main():
    print(f"\n{BLUE}{'#'*60}{RESET}")
    print(f"{BLUE}#  SCIRAG Setup Verification{RESET}")
    print(f"{BLUE}{'#'*60}{RESET}")
    
    # Check if we're in the right directory
    if not os.path.exists("backend") and not os.path.exists("docs"):
        print(f"\n{RED}Error: This script should be run from the SCIRAG root directory{RESET}")
        print("Navigate to your SCIRAG project folder and try again.")
        sys.exit(1)
    
    results = {
        "directories": check_directory_structure(),
        "init_files": check_init_files(),
        "poc_files": check_poc_files(),
        "documentation": check_documentation(),
        "gitignore": check_gitignore(),
        "venv": check_virtual_environment(),
        "env_config": check_environment_variables(),
        "poc_syntax": check_poc_imports(),
    }
    
    print_summary(results)
    
    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
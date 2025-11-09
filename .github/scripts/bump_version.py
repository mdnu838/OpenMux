#!/usr/bin/env python3
"""
Auto-increment version for CI/CD builds.
This script updates the patch version based on GitHub run number.
"""

import re
import sys
from pathlib import Path


def update_version_in_file(file_path: Path, old_version: str, new_version: str) -> bool:
    """Update version string in a file."""
    try:
        content = file_path.read_text()
        
        # Try different version patterns
        patterns = [
            (f'version = "{old_version}"', f'version = "{new_version}"'),
            (f"version = '{old_version}'", f"version = '{new_version}'"),
            (f'__version__ = "{old_version}"', f'__version__ = "{new_version}"'),
            (f"__version__ = '{old_version}'", f"__version__ = '{new_version}'"),
        ]
        
        updated = False
        for old_pattern, new_pattern in patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                updated = True
        
        if updated:
            file_path.write_text(content)
            print(f"✓ Updated {file_path}")
            return True
        else:
            print(f"⚠ No version pattern found in {file_path}")
            return False
            
    except Exception as e:
        print(f"✗ Error updating {file_path}: {e}")
        return False


def get_current_version(pyproject_path: Path) -> str:
    """Extract current version from pyproject.toml."""
    content = pyproject_path.read_text()
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in pyproject.toml")


def main():
    if len(sys.argv) < 2:
        print("Usage: bump_version.py <run_number>")
        sys.exit(1)
    
    run_number = sys.argv[1]
    
    # Paths
    root = Path(__file__).parent.parent.parent
    pyproject_path = root / "pyproject.toml"
    init_path = root / "openmux" / "__init__.py"
    
    # Get current version
    current_version = get_current_version(pyproject_path)
    print(f"Current version: {current_version}")
    
    # Parse version
    parts = current_version.split(".")
    if len(parts) != 3:
        print(f"✗ Invalid version format: {current_version}")
        sys.exit(1)
    
    major, minor, _ = parts
    
    # Create new version with run number as patch
    new_version = f"{major}.{minor}.{run_number}"
    print(f"New version: {new_version}")
    
    # Update files
    success = True
    success &= update_version_in_file(pyproject_path, current_version, new_version)
    success &= update_version_in_file(init_path, current_version, new_version)
    
    if success:
        print(f"\n✓ Version bumped from {current_version} to {new_version}")
        print(f"BUMPED_VERSION={new_version}")  # For GitHub Actions output
    else:
        print("\n✗ Version bump failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

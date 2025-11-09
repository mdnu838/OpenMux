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
        
        # Extract base version without suffix (e.g., "0.1.0-alpha" -> "0.1.0")
        base_old_version = old_version.split('-')[0]
        base_new_version = new_version.split('-')[0]
        
        # Use regex to handle version with optional suffixes
        patterns = [
            # For pyproject.toml: version = "x.y.z" or version = 'x.y.z'
            (re.compile(rf'(version\s*=\s*["\']){re.escape(old_version)}(["\'])'), 
             rf'\g<1>{new_version}\g<2>'),
            # For __init__.py: __version__ = "x.y.z" or __version__ = 'x.y.z' (with optional suffix)
            (re.compile(rf'(__version__\s*=\s*["\']){re.escape(base_old_version)}(-[a-zA-Z0-9]+)?(["\'])'), 
             rf'\g<1>{base_new_version}\g<3>'),
        ]
        
        updated = False
        for pattern, replacement in patterns:
            new_content, count = pattern.subn(replacement, content)
            if count > 0:
                content = new_content
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
    
    # Parse version (handle suffixes like -alpha, -beta)
    base_version = current_version.split('-')[0]
    parts = base_version.split(".")
    if len(parts) != 3:
        print(f"✗ Invalid version format: {current_version}")
        sys.exit(1)
    
    major, minor, _ = parts
    
    # Create new version with run number as patch (no suffix for CI builds)
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

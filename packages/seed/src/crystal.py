#!/usr/bin/env python3
"""
Bloom Crystal Packager
Production build system for Bloom applications.
"""

import sys
import os
import json
import hashlib
import time
import shutil
from pathlib import Path
import platform
import re

def get_platform_name():
    """Get platform-specific name for builds."""
    system = platform.system().lower()
    if system == "windows":
        return "win32"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def verify_root_seed():
    """Verify Root Seed for production builds."""
    print("[CRYSTAL] Production build requires Root Seed authorization")
    print("[CRYSTAL] This ensures only authorized deployments")

    # Read set.bloom to get the special code
    set_bloom_path = Path("set.bloom")
    if not set_bloom_path.exists():
        print("[ERROR] set.bloom not found. Run 'python cli/init.py' first.")
        return False, None

    with open(set_bloom_path, 'r') as f:
        content = f.read()

    # Extract the special code
    special_match = re.search(r'special:\s*"([^"]+)"', content)
    if not special_match:
        print("[ERROR] Special code not found in set.bloom")
        return False, None

    special_code = special_match.group(1)
    print(f"[CRYSTAL] Special code found: {special_code[:8]}...")

    # Prompt for Root Seed
    entered_seed = input("[CRYSTAL] Enter your Root Seed (BLM-XXXX-XXXX-XXXX-XXXX): ").strip()

    if entered_seed != special_code:
        print("[ERROR] Root Seed verification failed!")
        print("[CRYSTAL] Production build denied.")
        return False, None

    print("[SUCCESS] Root Seed verified. Proceeding with production build.")
    return True, special_code

def minify_json(data):
    """Minify JSON data."""
    return json.dumps(data, separators=(',', ':'))

def bundle_assets(build_dir):
    """Bundle all necessary assets for production."""
    print("[CRYSTAL] Bundling assets...")

    # Create build directory structure
    os.makedirs(build_dir / "assets", exist_ok=True)
    os.makedirs(build_dir / "engine", exist_ok=True)

    # Copy manifest
    manifest_src = Path("dist/manifest.json")
    manifest_dest = build_dir / "manifest.json"
    if manifest_src.exists():
        shutil.copy2(manifest_src, manifest_dest)
        print("[CRYSTAL] Manifest bundled")

    # Copy engine files
    engine_src = Path("engine")
    engine_dest = build_dir / "engine"
    if engine_src.exists():
        shutil.copytree(engine_src, engine_dest, dirs_exist_ok=True)
        print("[CRYSTAL] Engine files bundled")

    # Copy src directory for reference
    src_dest = build_dir / "src"
    shutil.copytree("src", src_dest, dirs_exist_ok=True)
    print("[CRYSTAL] Source files bundled")

def generate_signature(manifest_path, special_code, hardware_id):
    """Generate security signature for the build."""
    print("[CRYSTAL] Generating security signature...")

    # Read manifest
    with open(manifest_path, 'r') as f:
        manifest_content = f.read()

    # Create signature: Hash(Manifest + SpecialCode + HardwareID + Timestamp)
    signature_data = f"{manifest_content}{special_code}{hardware_id}{int(time.time())}"
    signature = hashlib.sha256(signature_data.encode()).hexdigest()

    print(f"[CRYSTAL] Signature generated: {signature[:16]}...")

    return signature

def create_production_config(build_dir, signature, app_type="standard"):
    """Create production configuration."""
    config = {
        "bloom_version": "0.1.0",
        "build_timestamp": int(time.time()),
        "platform": get_platform_name(),
        "app_type": app_type,
        "signature": signature,
        "features": {
            "ai_enabled": True,
            "local_first": True,
            "offline_capable": True
        }
    }

    config_path = build_dir / "bloom.config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print("[CRYSTAL] Production config created")

def optimize_manifest(build_dir):
    """Optimize and minify the production manifest."""
    manifest_path = build_dir / "manifest.json"
    if not manifest_path.exists():
        print("[ERROR] Manifest not found in build directory")
        return False

    # Read and minify
    with open(manifest_path, 'r') as f:
        manifest_data = json.load(f)

    # Add production optimizations
    manifest_data["production"] = True
    manifest_data["build_time"] = int(time.time())

    # Minify
    minified = minify_json(manifest_data)

    # Write back minified version
    with open(manifest_path, 'w') as f:
        f.write(minified)

    print(f"[CRYSTAL] Manifest optimized ({len(minified)} bytes)")

    return True

def create_launcher_script(build_dir, app_type):
    """Create platform-specific launcher script."""
    platform_name = get_platform_name()

    if platform_name == "win32":
        launcher_content = f'''@echo off
echo [BLOOM] Starting {app_type} application...
cd /d "%~dp0"
start engine\\preview.html
echo [BLOOM] Application launched. Press any key to exit.
pause > nul
'''
        launcher_path = build_dir / "launch.bat"
    else:
        launcher_content = f'''#!/bin/bash
echo "[BLOOM] Starting {app_type} application..."
cd "$(dirname "$0")"
if command -v python3 &> /dev/null; then
    python3 -m http.server 8080 &
    sleep 2
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8080/engine/preview.html
    elif command -v open &> /dev/null; then
        open http://localhost:8080/engine/preview.html
    fi
else
    echo "[ERROR] Python3 not found. Please install Python3."
    exit 1
fi
echo "[BLOOM] Application launched. Press Ctrl+C to stop."
trap "echo '[BLOOM] Application stopped.'" INT
wait
'''
        launcher_path = build_dir / "launch.sh"
        launcher_path.chmod(0o755)

    with open(launcher_path, 'w') as f:
        f.write(launcher_content)

    print(f"[CRYSTAL] Launcher script created for {platform_name}")

def main():
    if len(sys.argv) < 2 or sys.argv[1] != "--solidify":
        print("=" * 60)
        print("[CRYSTAL] Bloom Production Packager")
        print("=" * 60)
        print("Usage: python cli/crystal.py --solidify [app-type]")
        print("\nApp Types:")
        print("  news        - News feed application (BBC-style)")
        print("  gov         - Government portal (secure)")
        print("  standard    - Standard application (default)")
        print("\nExample: python cli/crystal.py --solidify news")
        return

    app_type = sys.argv[2] if len(sys.argv) > 2 else "standard"

    print("=" * 60)
    print("[CRYSTAL] Bloom Crystal Packager - Production Build")
    print("=" * 60)
    print(f"[CRYSTAL] Target: {app_type} application")

    # Step 1: Verify identity
    authorized, special_code = verify_root_seed()
    if not authorized:
        return

    # Step 2: Check if manifest exists
    manifest_path = Path("dist/manifest.json")
    if not manifest_path.exists():
        print("[ERROR] Manifest not found. Run 'python cli/sprout.py' first.")
        return

    # Step 3: Create build directory
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    print(f"[CRYSTAL] Build directory: {build_dir}")

    # Step 4: Bundle assets
    bundle_assets(build_dir)

    # Step 5: Optimize manifest
    if not optimize_manifest(build_dir):
        return

    # Step 6: Generate security signature
    # Get hardware ID (simplified - in production use proper hardware fingerprinting)
    hardware_id = platform.node() + str(platform.machine())
    signature = generate_signature(build_dir / "manifest.json", special_code, hardware_id)

    # Step 7: Create production config
    create_production_config(build_dir, signature, app_type)

    # Step 8: Create launcher
    create_launcher_script(build_dir, app_type)

    # Step 9: Create deployment summary
    summary = {
        "build_info": {
            "type": "production",
            "app_type": app_type,
            "platform": get_platform_name(),
            "timestamp": int(time.time()),
            "authorized_by": special_code[:8] + "..."
        },
        "security": {
            "signature": signature,
            "verification_required": True
        },
        "features": {
            "ai_enabled": True,
            "local_first": True,
            "offline_capable": True
        }
    }

    summary_path = build_dir / "build.summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("[SUCCESS] Crystal Build Complete!")
    print("=" * 60)
    print(f"[CRYSTAL] Build location: {build_dir.absolute()}")
    print(f"[CRYSTAL] App type: {app_type}")
    print(f"[CRYSTAL] Security signature: {signature[:16]}...")
    print("\n[CRYSTAL] To deploy:")
    if get_platform_name() == "win32":
        print(f"  - Run: {build_dir}/launch.bat")
    else:
        print(f"  - Run: ./{build_dir}/launch.sh")
    print("\n[CRYSTAL] Production build ready for distribution!")

if __name__ == "__main__":
    main()

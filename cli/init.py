#!/usr/bin/env python3
"""
Bloom Identity Generator
Creates your Root Seed and identity_lock for the Bloom project.
"""

import hashlib
import secrets
import platform
import uuid
import re
import os
from pathlib import Path


def generate_root_seed():
    """Generate a random 24-character Root Seed in format BLM-XXXX-XXXX."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    part1 = ''.join(secrets.choice(chars) for _ in range(4))
    part2 = ''.join(secrets.choice(chars) for _ in range(4))
    part3 = ''.join(secrets.choice(chars) for _ in range(4))
    part4 = ''.join(secrets.choice(chars) for _ in range(4))
    return f"BLM-{part1}-{part2}-{part3}-{part4}"


def get_hardware_id():
    """Capture a unique hardware ID from the computer."""
    # Use machine ID as hardware identifier
    try:
        # Try to get machine ID from platform-specific sources
        machine_id = platform.node() + str(uuid.getnode())
        # Hash it to get a consistent ID
        hardware_id = hashlib.sha256(machine_id.encode()).hexdigest()[:16]
        return hardware_id
    except Exception:
        # Fallback to random if hardware ID fails
        return secrets.token_hex(8)


def create_identity_lock(root_seed, hardware_id, name, recovery_answer):
    """Hash all components together to create identity_lock."""
    combined = f"{root_seed}{hardware_id}{name}{recovery_answer}"
    return hashlib.sha256(combined.encode()).hexdigest()[:32]


def parse_set_bloom(filepath):
    """Parse the set.bloom file and return it as a dictionary."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Simple parsing for the bloom config format
    config = {
        'special': 'nill',
        'recovery_question': 'nill',
        'identity_lock': 'nill'
    }
    
    return config


def update_set_bloom(filepath, special, recovery_question, identity_lock):
    """Update the set.bloom file with generated values."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace the security block values
    content = re.sub(
        r'special:\s*nill',
        f'special: "{special}"',
        content
    )
    content = re.sub(
        r'recovery_question:\s*nill',
        f'recovery_question: "{recovery_question}"',
        content
    )
    content = re.sub(
        r'identity_lock:\s*nill',
        f'identity_lock: "{identity_lock}"',
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)


def main():
    """Main execution flow."""
    print("=" * 60)
    print("🌸 BLOOM IDENTITY GENERATOR 🌸")
    print("=" * 60)
    print()
    
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    set_bloom_path = project_root / "set.bloom"
    
    if not set_bloom_path.exists():
        print(f"❌ Error: set.bloom not found at {set_bloom_path}")
        return
    
    # Generate Root Seed
    root_seed = generate_root_seed()
    print(f"🌱 Your Root Seed: {root_seed}")
    print("   ⚠️  WRITE THIS DOWN ON PAPER NOW!")
    print()
    
    # Capture Hardware ID
    hardware_id = get_hardware_id()
    print(f"🔒 Hardware ID: {hardware_id}")
    print()
    
    # Get user input
    print("Please provide the following information:")
    name = input("Your Name: ").strip()
    recovery_question = input("Secret Recovery Question: ").strip()
    recovery_answer = input("Answer to Recovery Question: ").strip()
    
    if not name or not recovery_question or not recovery_answer:
        print("❌ Error: All fields are required!")
        return
    
    print()
    
    # Create identity_lock
    identity_lock = create_identity_lock(root_seed, hardware_id, name, recovery_answer)
    print(f"🔐 Identity Lock: {identity_lock}")
    print()
    
    # Update set.bloom
    print("Updating set.bloom with your identity information...")
    update_set_bloom(set_bloom_path, root_seed, recovery_question, identity_lock)
    
    print()
    print("=" * 60)
    print("✅ SUCCESS! Your Bloom identity has been created.")
    print("=" * 60)
    print()
    print("IMPORTANT:")
    print("1. Your 'special' Root Seed is now in set.bloom")
    print("2. Write down your Root Seed on paper: " + root_seed)
    print("3. Keep your recovery question and answer safe")
    print("4. The identity_lock ensures only you can push updates")
    print()
    print("🌸 You're ready to start building with Bloom!")


if __name__ == "__main__":
    main()

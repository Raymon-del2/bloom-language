import os
import json
import re
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
SRC_FILE = "src/index.bloom"
DIST_DIR = "dist"
MANIFEST_FILE = os.path.join(DIST_DIR, "manifest.json")
SET_BLOOM = "set.bloom"

print("="*60)
print("[SPROUT] BLOOM SPROUT COMPILER (v0.2 Fixed)")
print("="*60)

# 1. VERIFY IDENTITY LOCK
# We check if the project has a lock, but we don't ask for the seed every time (annoying).
if not os.path.exists(SET_BLOOM):
    print("[ERROR] FATAL: set.bloom not found. Run 'bloom init' first.")
    exit(1)

with open(SET_BLOOM, "r") as f:
    if "identity_lock" not in f.read():
        print("[ERROR] SECURITY ERROR: No identity_lock found in set.bloom!")
        exit(1)
    else:
        print("[LOCK] Identity verified.")

# 2. HELPER: The "Smart" Parser
def clean_value(val):
    """
    Turns '20px' -> 20 (int)
    Turns 'true' -> True (bool)
    Turns 'neon' -> 'neon' (str)
    """
    if isinstance(val, bool):
        return val # It's already a boolean, don't touch it!
        
    val = str(val).strip()
    
    # Check for Boolean
    if val.lower() == "true": return True
    if val.lower() == "false": return False
    
    # Check for Numbers (with units like px, %, rem)
    # This regex finds the number part at the start
    number_match = re.match(r"^-?\d+(\.\d+)?", val)
    if number_match:
        # If the whole string is just a number/unit, return the number
        # e.g. "20px" -> 20. But "model-20" should stay a string.
        # We only strip if it looks like a measurement.
        if re.match(r"^-?\d+(\.\d+)?(px|rem|em|%)?$", val):
            try:
                if "." in number_match.group(0):
                    return float(number_match.group(0))
                return int(number_match.group(0))
            except:
                pass 
                
    return val

def parse_styles(style_string):
    """Parses 'padding: 20px; center: true;' into a dict"""
    if not style_string: return {}
    styles = {}
    # Split by semicolon, then by colon
    pairs = [s.split(":") for s in style_string.split(";") if ":" in s]
    for key, val in pairs:
        clean_key = key.strip()
        clean_val = clean_value(val) # <--- USE OUR CLEANER HERE
        styles[clean_key] = clean_val
    return styles

# 3. COMPILATION LOOP
try:
    print(f"[READ] Parsing {SRC_FILE}...")
    
    # We wrap the content in a root tag just in case standard XML parsers complain
    with open(SRC_FILE, "r", encoding="utf-8") as f:
        raw_content = f.read()
        
    # Python's XML parser hates standalone custom tags, so we wrap it
    # If your file already has a root, this might be redundant but safe
    if not raw_content.strip().startswith("<root>"):
        raw_content = f"<root>{raw_content}</root>"

    root = ET.fromstring(raw_content)
    
    compiled_nodes = []

    # Recursively find all elements
    for child in root.iter():
        if child.tag == "root": continue
        
        node = {
            "type": child.tag,
            "attributes": {},
            "content": child.text.strip() if child.text else None,
            "children": [] # Simple flat list for now
        }

        # Process Attributes (like id="main-btn")
        for k, v in child.attrib.items():
            if k == "style":
                # Special handling for CSS-like strings
                node["attributes"].update(parse_styles(v))
            else:
                node["attributes"][k] = clean_value(v)

        # AI-GENERATED CONTENT PROCESSING
        if "ai-generated" in node["attributes"] and node["attributes"]["ai-generated"] == "true":
            print(f"[AI] Processing AI-generated {node['type']} element")
            # AI content is already in the markup, just flag it
            node["attributes"]["ai_processed"] = "true"

        # SECURITY CHECK: Sieve Warning for Sensitive Actions
        if node["type"] == "button" and "action" in node["attributes"]:
            action = node["attributes"]["action"]
            if action in ["payment", "external_link"]:
                print(f"[WARN] SENSITIVE ACTION DETECTED: '{action}' will require Root Seed BLM-4WLS... for production deployment.")

        compiled_nodes.append(node)

    # 4. OUTPUT
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
        
    output_data = {
        "project": "Bloom-Alpha",
        "nodes": compiled_nodes
    }

    with open(MANIFEST_FILE, "w") as f:
        json.dump(output_data, f, indent=2)

    print("[SUCCESS] Sprout Complete!")
    print(f"[PACKAGE] Manifest saved to: {MANIFEST_FILE}")
    print(f"[FLOWER] Nodes generated: {len(compiled_nodes)}")

except Exception as e:
    print(f"[CRASH] COMPILER CRASHED: {e}")
    # Print the line that might have caused it (advanced debugging)
    import traceback
    traceback.print_exc()

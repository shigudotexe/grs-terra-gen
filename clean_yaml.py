import os
import sys
try:
    from ruamel.yaml import YAML
except ImportError:
    print("Error: 'ruamel.yaml' is missing. Run: pip install ruamel.yaml")
    sys.exit(1)

# Configure the cleaner
yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.width = 4096  # Prevents unwanted line wrapping

def clean_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
        
        if data is None:
            return

        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
        print(f" [CLEANED] {os.path.relpath(path)}")
    except Exception as e:
        print(f" [ERROR] Could not clean {path}: {e}")

# Recurse through the biomes folder
target_dir = 'biomes'
if os.path.exists(target_dir):
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".yml"):
                clean_file(os.path.join(root, file))
else:
    print(f"Directory '{target_dir}' not found.")

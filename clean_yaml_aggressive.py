import os
import sys
import re
try:
    from ruamel.yaml import YAML
except ImportError:
    print("Error: 'ruamel.yaml' is missing. Run: pip install ruamel.yaml")
    sys.exit(1)

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.width = 4096

def aggressive_clean(path):
    try:
        # 1. Standard YAML round-trip (normalizes indentation/structure)
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
        
        if data is None:
            return

        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)

        # 2. Regex Post-Processing (strips extra blank lines and trailing spaces)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove trailing whitespace from every line
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
        
        # Collapse 3 or more newlines into just 2 (resulting in 1 blank line)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Ensure the file doesn't end with a massive block of newlines
        content = content.strip() + '\n'

        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
            
        print(f" [AGGRESSIVE CLEAN] {os.path.relpath(path)}")
    except Exception as e:
        print(f" [ERROR] Could not clean {path}: {e}")

target_dir = 'biomes'
if os.path.exists(target_dir):
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".yml"):
                aggressive_clean(os.path.join(root, file))
else:
    print(f"Directory '{target_dir}' not found.")

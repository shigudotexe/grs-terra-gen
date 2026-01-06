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

def move_veins_to_ores(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
        
        if data is None or 'features' not in data:
            return

        features = data['features']
        changed = False

        # Check if 'veins' exists and is not empty
        if 'veins' in features and features['veins']:
            vein_content = features['veins']
            
            # Ensure 'ores' exists
            if 'ores' not in features or features['ores'] is None:
                features['ores'] = []
            
            # Move content: handle if veins is a list or a single item
            if isinstance(vein_content, list):
                for item in vein_content:
                    if item not in features['ores']:
                        features['ores'].append(item)
            else:
                if vein_content not in features['ores']:
                    features['ores'].append(vein_content)
            
            # Remove the veins key
            del features['veins']
            changed = True

        if changed:
            # Save the YAML structure
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f)

            # Aggressive Clean: Post-process newlines and spaces
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE) # Strip trailing spaces
            content = re.sub(r'\n{3,}', '\n\n', content)                # Collapse newlines
            content = content.strip() + '\n'                            # Final trim

            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            
            print(f" [FIXED ORES] {os.path.relpath(path)}")
            
    except Exception as e:
        print(f" [ERROR] {path}: {e}")

# Recurse through biomes folder
target_dir = 'biomes'
if os.path.exists(target_dir):
    print("Scanning for 'veins' to migrate to 'ores'...")
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".yml"):
                move_veins_to_ores(os.path.join(root, file))
    print("Done.")
else:
    print(f"Directory '{target_dir}' not found.")

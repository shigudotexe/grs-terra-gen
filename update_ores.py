import os
import re
import sys
try:
    from ruamel.yaml import YAML
except ImportError:
    print("Error: 'ruamel.yaml' is missing. Run: pip install ruamel.yaml")
    sys.exit(1)

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

ORE_MAPPING = {
    "BEACH": "IRON_BOULDERS",
    "VOLCANO": "COAL_BOULDERS",
    "POLAR": "EMERALD_BOULDERS",
    "DESERT": "GOLD_BOULDERS",
    "COLD MOUNTAIN": "EMERALD_BOULDERS",
    "TEMPERATE MOUNTAIN": "REDSTONE_BOULDERS",
    "WARM MOUNTAIN": "LAPIS_BOULDERS",
    "HOT MOUNTAIN": "GOLD_BOULDERS",
    "WARM FLATLAND": "COPPER_BOULDERS",
    "HOT FLATLAND": "COPPER_BOULDERS",
    "WARM FOREST": "COAL_BOULDERS",
    "COLD FLATLAND": "COAL_BOULDERS",
    "COLD FOREST": "COAL_BOULDERS",
    "TEMPERATE FLATLAND": "COPPER_BOULDERS",
    "TEMPERATE FOREST": "COPPER_BOULDERS",
    "OCEAN": "COPPER_BOULDERS",
    "MUSHROOM": "COPPER_BOULDERS",
    "CHERRY FOREST": "COAL_BOULDERS",
    "HOT FOREST": "COPPER_BOULDERS"
}

def parse_category_file(file_path):
    biome_to_category = {}
    current_category = None
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            header_match = re.search(r'#####\s*(.*?)\s*#####', line)
            if header_match:
                current_category = header_match.group(1).upper()
                continue
            if line.endswith('.yml') and current_category:
                # Get the filename without .yml
                biome_id = line.split('/')[-1].replace('.yml', '')
                biome_to_category[biome_id] = current_category
    return biome_to_category

def modify_biome_file(path, boulder_string):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
        
        # If file is empty or invalid
        if data is None:
            data = {}

        # 1. Ensure 'features' exists as a dictionary
        if 'features' not in data or data['features'] is None:
            data['features'] = {}
            
        # 2. Ensure 'landforms' exists as a list under 'features'
        if 'landforms' not in data['features'] or data['features']['landforms'] is None:
            data['features']['landforms'] = []
        
        # 3. Inject if not present
        if boulder_string not in data['features']['landforms']:
            data['features']['landforms'].append(boulder_string)
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f)
            print(f" [UPDATED] {os.path.relpath(path)} -> {boulder_string}")
        else:
            print(f" [SKIPPED] {os.path.relpath(path)} already has {boulder_string}")

    except Exception as e:
        print(f" [ERROR] {path}: {e}")

# EXECUTION
mapping_file = 'Biome_Types V2.1(2).txt'
biome_map = parse_category_file(mapping_file)

if biome_map:
    # Recursively check the main biomes folder
    # This covers aquatic, land, other, etc.
    for root, _, files in os.walk('biomes'):
        # Safety: exclude the cave folder if you want zero changes there
        if 'cave' in root.lower():
            continue

        for file in files:
            if file.endswith(".yml"):
                biome_id = file.replace(".yml", "")
                cat = biome_map.get(biome_id)
                if cat in ORE_MAPPING:
                    modify_biome_file(os.path.join(root, file), ORE_MAPPING[cat])

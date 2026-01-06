# Ore Redistribution Changes - Aggressive Rebalancing

**Date**: December 26, 2025  
**Backup Created**: `features/deposits/distribution.yml.backup`  
**Changes**: Biome-level ore assignments only (spawn rates unchanged)

---

## Changes Summary

### 1. **Badlands** - Gold becomes primary ore
**File**: `biomes/abstract/features/ores/ores_badlands.yml`

**Before:**
- Common: Iron (IRON_ORE_HIGH)
- Rare: Gold (GOLD_ORE_UNIFORM)
- Sparse: Copper, Coal

**After:**
- Common: Gold (GOLD_ORE + GOLD_ORE_UNIFORM) ✨
- Uncommon: Iron (IRON_ORE_HIGH)
- Sparse: Coal

**Rationale**: Badlands exposed rock formations thematically fit gold veins better than iron. Removes one major Iron source (biome clusters). Copper sparse removed (already in deserts).

---

### 2. **Polar/Frozen** - Gold and Emerald replace Iron
**File**: `biomes/abstract/features/ores/ores_frozen.yml`

**Before:**
- Common: Iron (IRON_ORE_UNIFORM)
- Rare: Diamond
- Sparse: Copper, Coal

**After:**
- Common: Gold (GOLD_ORE_UNIFORM) ✨
- Uncommon: Emerald ✨
- Rare: Diamond
- Sparse: Coal

**Rationale**: Removes second major Iron source. Gold "glacial alluvial deposits" makes thematic sense. Emerald "crystal formations in glaciers" adds variety. Removes Copper sparse (less needed in polar).

---

### 3. **Ocean** - Lapis becomes primary ore
**File**: `biomes/abstract/features/ores/ores_ocean.yml`

**Before:**
- Common: Copper (COPPER_ORE_VEINS)
- Rare: Lapis (LAPIS_ORE_UNIFORM)
- Sparse: Coal

**After:**
- Common: Lapis (LAPIS_ORE_UNIFORM + LAPIS_ORE) ✨
- Rare: Copper (COPPER_ORE_VEINS)
- Sparse: Coal

**Rationale**: Major Copper reduction. Ocean floor sedimentary deposits thematically fit Lapis perfectly. Makes Lapis more accessible.

---

### 4. **Tropical Humid (Jungle)** - Gold added as uncommon ore
**File**: `biomes/abstract/features/ores/ores_tropical_humid.yml`

**Before:**
- Common: Lapis
- Rare: Diamond
- Sparse: Copper, Coal

**After:**
- Common: Lapis
- Uncommon: Gold (GOLD_ORE) ✨
- Rare: Diamond
- Sparse: Coal

**Rationale**: Tropical is 32.6% of all biomes - adds reward for jungle exploration. "Hidden treasure" theme fits jungle. Removes Copper sparse (redundant with neighboring biomes). Makes Gold more available.

---

### 5. **Boreal Mountains** - Gold added as uncommon ore
**File**: `biomes/abstract/features/ores/ores_mountain.yml`

**Before:**
- Common: Iron (IRON_ORE + IRON_ORE_HIGH)
- Rare: Emerald
- Sparse: Copper, Coal

**After:**
- Common: Iron (IRON_ORE + IRON_ORE_HIGH)
- Uncommon: Gold (GOLD_ORE) ✨
- Rare: Emerald
- Sparse: Copper, Coal

**Rationale**: Mountains remain Iron-focused (thematic). Gold adds diversity without breaking theme. Keeps all sparse ores for flexibility.

---

## Impact Analysis

### Iron Reduction
- **Removed from**: Badlands, Polar
- **Still found in**: Temperate Forest, Continental Humid, Boreal Forest, Boreal Mountains
- **Impact**: ~33% fewer biomes have primary Iron access
- **Benefit**: Iron still abundant, but requires more intentional traveling

### Copper Reduction
- **Removed from**: Badlands, Polar, Tropical Humid
- **Still found in**: Ocean (now rare), Continental Monsoon, Subtropical Humid, Mountains (sparse)
- **Impact**: ~40% fewer copper-heavy sources
- **Benefit**: Copper still findable, less oversaturation

### Gold Increase
- **Added to**: Badlands (primary), Polar (primary), Tropical Humid, Mountains
- **Impact**: 4 new biome sources vs. 3 original (Desert, Coastal, Volcanic)
- **Benefit**: Gold now feels achievable, rewards exploration across climates

### Lapis Increase
- **Added to**: Ocean (primary)
- **Impact**: 2 new Lapis sources (Ocean is large biome type)
- **Benefit**: Much more accessible, less niche

### Emerald Increase
- **Added to**: Polar
- **Impact**: 3 sources now (Mountains, Tropical Monsoon, Polar)
- **Benefit**: More distributed, less concentrated in one region

---

## Biome Coverage (After Changes)

| Ore Type | Biome Count | Coverage |
|----------|------------|----------|
| Iron | 4 | Temperate Forest, Continental Humid, Boreal Forest, Boreal Mountains |
| Copper | 4 | Ocean (rare), Continental Monsoon, Subtropical Humid, Mountains (sparse) |
| Gold | 7 | **Badlands, Polar, Tropical Humid, Mountains, Desert, Coastal, Volcanic** |
| Lapis | 3 | **Ocean, Tropical Humid, Jungle** |
| Emerald | 3 | Mountains, Subtropical Monsoon, **Polar** |
| Coal | All | Savanna, Temperate, Subarctic, Mountains, Plains, etc. |
| Redstone | 3 | Boreal Forest, Mushroom, Wetlands |
| Diamond | 2 | Cave, Polar |

---

## Testing Recommendations

1. **Generate new chunks** - Old chunks won't update
2. **Test in Badlands** - Should see Gold prominently
3. **Test in Ocean** - Should see less Copper, more Lapis
4. **Test in Tropical** - Should find Gold in jungles
5. **Test in Polar** - Should see less Iron, more Gold
6. **Mine vertically** - Track ore encounter rates

---

## Rollback Instructions

If changes feel wrong:
```
1. Delete modified ore files
2. Copy from .backup files
3. Or restore git commit
```

All changes are in `biomes/abstract/features/ores/` directory.

---

## Future Tweaks

If needed, can also:
- Adjust spawn rates in `distribution.yml` (unchanged in this pass)
- Create ore variants (e.g., `GOLD_ORE_ENHANCED`)
- Fine-tune specific biome distributions
- Add ore indicators (surface ores) as needed

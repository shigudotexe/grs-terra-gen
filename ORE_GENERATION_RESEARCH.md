# Terra v6 Ore Generation Configuration Research

## Summary
Yes, you **can** make ores generate more towards cave walls and in more exposed areas in Terra v6. The configuration system provides several mechanisms to achieve this.

---

## Current Ore System Structure

### How Ores Currently Work
The Terra default pack uses a two-layer system:

1. **Feature Configs** (`features/deposits/ores/*.yml`)
   - Define WHEN and WHERE ores spawn (distributors & locators)
   - Use `GAUSSIAN_RANDOM` or `POSITIVE_WHITE_NOISE` distribution
   - Currently: Random placement throughout defined Y-ranges

2. **Structure Configs** (`structures/deposits/ores/*.yml`)
   - Define the SHAPE and SIZE of ore veins
   - Currently: Use `TEARDROP` shape, size ~7-18 blocks
   - Only replace `minecraft:stone` and `minecraft:deepslate`

3. **Distribution Config** (`features/deposits/distribution.yml`)
   - Centralized Y-level ranges and spawn rates per chunk
   - Completely horizontal random distribution (no cave awareness)

### Example Current Configuration
```yaml
# features/deposits/ores/iron_ore.yml
locator:
  type: GAUSSIAN_RANDOM    # ← Random Y-height selection
  amount: 1
  height: *range           # ← Only controls vertical range
  standard-deviation: *standard-deviation

# Uses POSITIVE_WHITE_NOISE sampler for 2D random placement
```

---

## Solutions to Generate Ores More in Exposed Areas

### Option 1: Use ADJACENT_PATTERN Locator (RECOMMENDED)
**Most direct approach** - Only place ore where adjacent air blocks exist (cave walls)

```yaml
locator:
  type: ADJACENT_PATTERN
  pattern:
    type: MATCH_AIR      # ← Match air blocks adjacent to placement
    offset: 0..3         # ← Check nearby blocks for air
  range: *range          # ← Vertical range
  match-all: false       # ← Only need some air blocks adjacent
```

**Pros:**
- Native Terra feature designed for this
- Minimal performance impact
- Works with existing ore sizes/shapes

**Cons:**
- Will only place in actual caves, not cliff faces without air
- Requires some adjacent air exposure

---

### Option 2: Use SURFACE Locator (For Top/Edge Placement)
**Places ores at surface level or height transitions**

```yaml
locator:
  type: SURFACE
  range: *range  # ← Search for solid-to-air transitions
```

**Pros:**
- Places at natural boundaries
- Works for cliff faces, terrain edges

**Cons:**
- Less suitable for deep cave placement
- Limits to actual surface boundaries

---

### Option 3: Use SAMPLER_3D with Conditional Noise
**Most flexible** - Use 3D noise samplers to bias placement toward exposed areas

```yaml
locator:
  type: SAMPLER_3D
  sampler:
    type: FRACTAL
    function: CUBIC
    octaves: 2
    frequency: 0.1  # ← Adjust to control clustering near caves
```

**Pros:**
- Very customizable
- Can create natural clustering patterns
- Works with arbitrary terrain shapes

**Cons:**
- More complex configuration
- Requires tuning for best results

---

### Option 4: Combine Multiple Locators with AND/OR
**Hybrid approach** - Place ore in multiple conditions

```yaml
locator:
  type: OR
  locators:
    - type: ADJACENT_PATTERN
      pattern:
        type: MATCH_AIR
        offset: 0..3
      range: *range
    - type: GAUSSIAN_RANDOM
      height: *range
      standard-deviation: *standard-deviation
      amount: 1
```

This places ores either:
- Where cave walls exist (adjacent air), OR
- In random hidden deposits

---

## Additional Configuration Options

### 1. Adjust Size/Shape for Cave Placement
Current ore shapes (`TEARDROP`) work fine, but you could:
- **Increase ore size** slightly for cave visibility
- **Use custom TerraScript** for shape adjustments

### 2. Create Separate Ore Features
Add dedicated "cave ore" variants:

```yaml
# features/deposits/ores/iron_ore_cave.yml
id: IRON_ORE_CAVE
type: FEATURE

# Same as regular iron, but with:
distributor:
  type: SAMPLER
  sampler: POSITIVE_WHITE_NOISE
  threshold: 0.003  # ← Much lower threshold (rarer)

locator:
  type: ADJACENT_PATTERN
  pattern:
    type: MATCH_AIR
    offset: 0..2
  range: -60..-24  # ← Biased toward caves
```

Then add to biome configs as "cave ore" variants.

### 3. Increase Density/Count Per Chunk
In `distribution.yml`:
```yaml
iron:
  averageCountPerChunk: 2.25  # ← Increase this value
  # Higher = more ore deposits per chunk
```

---

## Implementation Steps

If you want to modify ore placement:

1. **Backup original configs:**
   ```
   features/deposits/ores/
   structures/deposits/ores/
   ```

2. **Edit ore feature files:**
   - Replace `GAUSSIAN_RANDOM` with `ADJACENT_PATTERN` locator
   - Add pattern matching for air blocks

3. **Test in-game:**
   - Generate new chunks to see changes
   - Observe cave ore visibility

4. **Optional: Create cave-specific variants:**
   - Duplicate ore configs with `_CAVE` suffix
   - Use exposed-area patterns
   - Add to mountain/cave biomes

---

## Technical Constraints & Notes

**What Terra v6 CAN do:**
- ✅ Match adjacent blocks (air, solid, specific types)
- ✅ Use 3D noise for spatial distribution
- ✅ Combine multiple placement conditions (AND/OR)
- ✅ Limit placement by Y-height ranges
- ✅ Use surface-based locators

**What Terra v6 CANNOT do natively:**
- ❌ Direct carving algorithm integration
- ❌ Per-cave targeted placement (caves are generated separately)
- ❌ Real-time cave detection

**Workaround for cave preference:**
Use `ADJACENT_PATTERN` with `MATCH_AIR` - this effectively makes ores "prefer" exposed areas since caves have air blocks adjacent to solid stone.

---

## Recommended Configuration

For ores biased toward exposed/cave areas:

```yaml
locator:
  type: ADJACENT_PATTERN
  pattern:
    type: MATCH_AIR
    offset: 0..2
  range: *range
  match-all: false  # ← Doesn't need ALL adjacent blocks to be air
```

This provides:
- Natural cave wall clustering
- Cliff face placement
- Minimal performance impact
- Easy to implement (copy-paste change)

---

## Files to Modify

Start with these if implementing:
- `features/deposits/ores/iron_ore.yml`
- `features/deposits/ores/diamond_ore.yml`
- `features/deposits/ores/lapis_ore.yml`
- (or create new `*_cave.yml` variants)

Then add the new variants to biome feature lists:
- `biomes/abstract/features/ores/*.yml`

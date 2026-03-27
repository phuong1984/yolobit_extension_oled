# Robot Eyes OLED - Animation Documentation

## Overview

This document describes all animation behaviors for the custom eyes OLED extension. Each expression has three animation modes: **Idle**, **Move**, and **Action**, plus an **All** mode that cycles through them.

---

## Animation Modes

| Mode | Description | Duration |
|------|-------------|----------|
| `idle` | Stay in place with expression-specific idle animation | Continuous |
| `move` | Travel around screen with bounce movement | Continuous |
| `action` | Perform expression-specific special action | ~60 frames (loop) |
| `all` | Cycle: idle (2s) → move (3s) → action → repeat | Continuous |

---

## Expression Animation Table

### 😐 Normal

| Mode | Behavior |
|------|----------|
| **Idle** | Random blink every ~100 frames |
| **Move** | Bounce around screen (speed: 1x, 1y) |
| **Action** | Look around: left → center → right → center |

---

### 😊 Happy

| Mode | Behavior |
|------|----------|
| **Idle** | Slight bounce up/down (3px amplitude) |
| **Move** | Fast bounce around screen (speed: 2x, 2y) |
| **Action** | Big smile bounce (5px amplitude, wide smile) |

---

### 😢 Sad

| Mode | Behavior |
|------|----------|
| **Idle** | Looking down (pupil dy=3), slow blink every ~150 frames |
| **Move** | Slow bounce around screen (speed: 1x, 1y) |
| **Action** | Slow close and open eyes (30 frames close, 30 frames open) |

---

### 😠 Angry

| Mode | Behavior |
|------|----------|
| **Idle** | Slight shake (1px every 20 frames) |
| **Move** | Fast jerky bounce (speed: 3x, 2y) |
| **Action** | Intense shake (3px x, 2px y, pupils down) |

---

### 😲 Surprised

| Mode | Behavior |
|------|----------|
| **Idle** | Quick blinks every ~60 frames (5 frames closed) |
| **Move** | Quick vertical bounce (speed: 2x, 3y) |
| **Action** | Jump and shake (10px jump + 2px shake) |

---

### 😴 Sleepy

| Mode | Behavior |
|------|----------|
| **Idle** | Slowly closing eyes (cycle: 150-200 frames), "zzz" text |
| **Move** | Very slow horizontal drift only (speed: 1x, 0y) |
| **Action** | Fully close → hold → slowly open (40+40+20 frames) |

---

### 😉 Wink

| Mode | Behavior |
|------|----------|
| **Idle** | Occasional wink (right eye closed 20% of time) |
| **Move** | Playful fast bounce (speed: 2x, 2y) |
| **Action** | Double wink (alternate eyes every 20 frames) |

---

### 😍 Love

| Mode | Behavior |
|------|----------|
| **Idle** | Heart pulse (2px amplitude on Y axis) |
| **Move** | Smooth bounce (speed: 2x, 2y) |
| **Action** | Hearts float up from eyes (pulse + floating heart pixels) |

---

### 👀 Look Left

| Mode | Behavior |
|------|----------|
| **Idle** | Pupils stay left (dx=-5) + random blink every ~100 frames |
| **Move** | Bounce around screen (speed: 2x, 2y), pupils stay left |
| **Action** | Glance: far left (dx=-8) → mid left (dx=-4) → center (dx=0) |

---

### 👀 Look Right

| Mode | Behavior |
|------|----------|
| **Idle** | Pupils stay right (dx=5) + random blink every ~100 frames |
| **Move** | Bounce around screen (speed: 2x, 2y), pupils stay right |
| **Action** | Glance: far right (dx=8) → mid right (dx=4) → center (dx=0) |

---

## Movement System

### Bounce Movement

All `move` animations use a **bounce movement** system:

1. **Velocity-based**: Position updates by velocity each frame
2. **Screen limits**: Calculated based on eye size to keep all features visible
3. **Direction reversal**: Velocity reverses when hitting screen edges

### Speed Settings

| Expression | Speed X | Speed Y | Notes |
|------------|---------|---------|-------|
| Normal | 1 | 1 | Standard pace |
| Happy | 2 | 2 | Energetic |
| Sad | 1 | 1 | Slow, lethargic |
| Angry | 3 | 2 | Fast, aggressive |
| Surprised | 2 | 3 | Jumpy, vertical focus |
| Sleepy | 1 | 0 | Horizontal drift only |
| Wink | 2 | 2 | Playful |
| Love | 2 | 2 | Smooth |
| Look Left | 2 | 2 | Pupils stay left |
| Look Right | 2 | 2 | Pupils stay right |

### Screen Limits Calculation

```
X limits (based on eye width `ew`):
  Left:  x >= -32 + ew/2 + 2
  Right: x <= 32 - ew/2 - 2

Y limits (based on eye height `eh`):
  Up:    y >= -(24 - eh/2 - 2)   [brow stays >= 0]
  Down:  y <= 8                   [mouth stays <= 64]
```

---

## Usage Example

```python
from eyes import Eyes
from animations import set_custom_eyes_config, animate_custom_eyes
import time

# Initialize
e = Eyes(scl_pin=Pin(22), sda_pin=Pin(21))

# Set custom expression (call once in init)
set_custom_eyes_config(
    expr='angry',
    ew=40, eh=40, rx=10, pupil='medium'
)

# In main loop
while True:
    animate_custom_eyes(e, mode='all')  # or 'idle', 'move', 'action'
    time.sleep_ms(50)  # ~20 FPS
```

---

## Block Usage (Blockly)

### Block 1: Set Custom Expression
```
🤖 Custom eyes  Face: [angry v]  Eye width: [40] px  Eye height: [40] px  
               Corner: [10] px  Pupil: [medium v]
```
*Use in initialization/setup*

### Block 2: Animate Custom Eyes
```
🎬 Animate custom eyes [all v]
```
*Use in `while True` loop*

Dropdown options:
- `idle` — Stay in place
- `move` — Travel around
- `action` — Special behavior
- `all` — Cycle through all

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-26 | 1.0 | Initial documentation |
| 2026-03-26 | 1.1 | Added random blink to look_left/look_right idle |
| 2026-03-26 | 1.2 | Changed move system to bounce movement with edge detection |

---

## Notes for Developers

When modifying animations:

1. **Keep within screen limits**: Use `_get_move_limits()` for calculations
2. **Mouth follows eyes**: Always pass `x_offset` and `y_offset` to `_draw_custom_mouth()`
3. **Brow follows eyes**: Always pass offsets to `_draw_custom_brow()`
4. **Update this doc**: When changing animation behavior, update this file

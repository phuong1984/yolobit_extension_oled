# animations.py — Robot eyes animation sequences
# Requires: eyes.py, expressions.py
# Each animation runs on an Eyes instance with configurable repeat count.

from eyes import Eyes, EYE_L_CX, EYE_R_CX, EYE_CY, EYE_W, EYE_H, PUPIL_R, SCREEN_W
from expressions import show_expression, EXPRESSIONS, expr_normal
import time
import math
import random
import gc


# ================================================================== #
#  PRE-COMPUTED FRAMES (memory optimization)                          #
# ================================================================== #

# Blink close/open percentages (reused, no allocation in loop)
_BLINK_CLOSE = (0.3, 0.6, 0.85, 1.0)
_BLINK_OPEN = (0.7, 0.4, 0.15, 0.0)

# Look around sequence (pre-computed)
_LOOK_AROUND_SEQUENCE = [(-6, 0), (0, 0), (6, 0), (0, 0), (0, -4), (0, 4), (0, 0)]

# Dizzy frames (pre-computed circle positions)
_DIZZY_FRAMES = [
    (int(5 * math.cos(2 * math.pi * i / 12)),
     int(4 * math.sin(2 * math.pi * i / 12)))
    for i in range(12)
]

# Wake up stages (pre-computed)
_WAKE_UP_STAGES = [
    (1, True,  False),  # (top_clip, half_open, normal)
    (1, True,  False),
    (0, True,  False),
    (0, False, False),  # normal
]


# ================================================================== #
#  BLINK ANIMATION                                                    #
# ================================================================== #

def anim_blink(e: Eyes, times=1, speed=1.0):
    """
    Natural blink: close → open with easing.
    speed: 1.0 = normal, 2.0 = fast, 0.5 = slow
    """
    delay = int(30 / speed)
    hold_delay = int(60 / speed)
    
    for _ in range(times):
        # Close
        for close_pct in _BLINK_CLOSE:
            e.clear()
            clip = int(EYE_H * close_pct)
            _draw_closing_eyes(e, clip)
            e.show()
            time.sleep_ms(delay)
        # Hold closed briefly
        time.sleep_ms(hold_delay)
        # Open
        for close_pct in _BLINK_OPEN:
            e.clear()
            clip = int(EYE_H * close_pct)
            _draw_closing_eyes(e, clip)
            e.show()
            time.sleep_ms(delay)
    
    gc.collect()


def _draw_closing_eyes(e: Eyes, clip_amount: int):
    """Helper: draw eyes partially closed based on clip_amount."""
    for cx in (EYE_L_CX, EYE_R_CX):
        e.draw_eye(cx, EYE_CY,
                   bot_clip=clip_amount,
                   top_clip=max(0, clip_amount - EYE_H // 2))
    e.draw_mouth(smile=0, width=18)


# ================================================================== #
#  IDLE BLINK (auto-blink with random timing)                         #
# ================================================================== #

def anim_idle(e: Eyes, times=1, speed=1.0):
    """
    Run an expression with random auto-blinks.
    times: number of blink cycles to perform
    speed: affects blink speed (1.0 = normal, 2.0 = fast, 0.5 = slow)
    """
    # Run for a fixed duration per times unit (5 seconds per times)
    duration_ms = 5000 * times
    expression = "normal"

    show_expression(e, expression)
    start = time.ticks_ms()
    next_blink = time.ticks_ms() + random.randint(2000, 4000)

    while time.ticks_diff(time.ticks_ms(), start) < duration_ms:
        now = time.ticks_ms()
        if time.ticks_diff(now, next_blink) >= 0:
            anim_blink(e, speed=speed)
            show_expression(e, expression)
            next_blink = time.ticks_ms() + random.randint(2000, 5000)
        time.sleep_ms(50)
    
    gc.collect()


# ================================================================== #
#  LOOK AROUND                                                        #
# ================================================================== #

def anim_look_around(e: Eyes, times=1, speed=1.0):
    """Eyes scan left → right → up → down → center."""
    delay = int(200 / speed)
    
    for _ in range(times):
        for dx, dy in _LOOK_AROUND_SEQUENCE:
            e.clear()
            e.draw_both_eyes(pupil_dx=dx, pupil_dy=dy)
            e.draw_mouth(smile=0, width=18)
            e.show()
            time.sleep_ms(delay)
    
    gc.collect()


# ================================================================== #
#  DIZZY                                                              #
# ================================================================== #

def anim_dizzy(e: Eyes, times=2, speed=1.0):
    """Pupils rotate in circles — dizzy effect."""
    delay = int(60 / speed)
    
    for _ in range(times):
        for dx, dy in _DIZZY_FRAMES:
            e.clear()
            e.draw_both_eyes(pupil_dx=dx, pupil_dy=dy)
            # Dizzy spiral marks
            e.oled.hline(54, 20, 4, 1)
            e.oled.hline(70, 16, 4, 1)
            e.show()
            time.sleep_ms(delay)
    
    gc.collect()


# ================================================================== #
#  WAKE UP                                                            #
# ================================================================== #

def anim_wake_up(e: Eyes, times=1, speed=1.0):
    """Transition from sleepy to normal with gradual eye opening."""
    delay = int(80 / speed)
    
    for _ in range(times):
        for top, half, _ in _WAKE_UP_STAGES:
            e.clear()
            e.draw_eye(EYE_L_CX, EYE_CY, half_open=half)
            e.draw_eye(EYE_R_CX, EYE_CY, half_open=half)
            e.show()
            time.sleep_ms(delay)
        # Final blink
        anim_blink(e)
        show_expression(e, "normal")
    
    gc.collect()


# ================================================================== #
#  SHOCKED (quick surprised reaction)                                 #
# ================================================================== #

def anim_shocked(e: Eyes, times=1, speed=1.0):
    """Quick: normal → blink → surprised with jolt."""
    for _ in range(times):
        show_expression(e, "normal")
        time.sleep_ms(int(100 / speed))
        anim_blink(e)
        show_expression(e, "surprised")
        # Tiny shake
        for _ in range(4):
            e.oled.scroll(2, 0)
            e.show()
            time.sleep_ms(int(30 / speed))
            e.oled.scroll(-2, 0)
            e.show()
            time.sleep_ms(int(30 / speed))
    
    gc.collect()


# ================================================================== #
#  HAPPY BOUNCE                                                       #
# ================================================================== #

def anim_happy_bounce(e: Eyes, times=3, speed=1.0):
    """Bounce pupils upward with each happy pulse."""
    delay = int(100 / speed)
    
    for _ in range(times):
        show_expression(e, "happy")
        time.sleep_ms(delay)
        e.clear()
        e.draw_both_eyes(pupil_dy=-3)
        e.draw_mouth(smile=10, width=28)
        e.show()
        time.sleep_ms(delay)
    show_expression(e, "happy")
    
    gc.collect()


# ================================================================== #
#  ANIMATION REGISTRY                                                 #
# ================================================================== #

ANIMATIONS = {
    "blink":        anim_blink,
    "idle":         anim_idle,
    "look_around":  anim_look_around,
    "dizzy":        anim_dizzy,
    "wake_up":      anim_wake_up,
    "shocked":      anim_shocked,
    "happy_bounce": anim_happy_bounce,
}


def play_animation(eyes: Eyes, name: str, times=1, speed=1.0, **kwargs):
    """
    Play a named animation.
    Example: play_animation(e, "blink", times=2, speed=1.5)
    """
    fn = ANIMATIONS.get(name)
    if fn is None:
        raise ValueError("Unknown animation: {}".format(name))
    fn(eyes, times=times, speed=speed, **kwargs)
    gc.collect()  # Final cleanup after animation


# ================================================================== #
#  DRAW HELPERS reused from eyes module                               #
# ================================================================== #

# ================================================================== #
#  DRAW HELPERS reused from eyes module                               #
# ================================================================== #

def _draw_mouth_on(e, smile=0, width=18):
    e.draw_mouth(smile=smile, width=width)


# ================================================================== #
#  CUSTOM EYES ANIMATION (NON-BLOCKING)                               #
# ================================================================== #

# Global state for custom eyes animation
_CUSTOM_EYES_CONFIG = {
    'expr': 'normal',
    'ew': 28,
    'eh': 28,
    'rx': 10,
    'pupil': 'medium'
}

_CUSTOM_ANIM_STATE = {
    'mode': 'idle',
    'phase': 'idle',  # idle, move, action
    'x_offset': 0,
    'y_offset': 0,
    'vx': 1,  # velocity X for bounce movement
    'vy': 1,  # velocity Y for bounce movement
    'frame': 0,
    'last_switch': 0,
    'idle_duration': 2000,   # 2 seconds
    'move_duration': 3000,   # 3 seconds
    'action_frame': 0,
    'action_complete': False
}


def set_custom_eyes_config(expr='normal', ew=28, eh=28, rx=10, pupil='medium'):
    """Store custom eyes configuration for animation."""
    global _CUSTOM_EYES_CONFIG
    _CUSTOM_EYES_CONFIG = {
        'expr': expr,
        'ew': int(ew),
        'eh': int(eh),
        'rx': int(rx),
        'pupil': pupil
    }


def _get_pupil_r():
    """Get pupil radius based on config."""
    from expressions import _pupil_r_for
    es = min(_CUSTOM_EYES_CONFIG['ew'], _CUSTOM_EYES_CONFIG['eh'])
    return int(_pupil_r_for(es, _CUSTOM_EYES_CONFIG['pupil']))


def _draw_custom_eyes_at(e, cx, cy, pupil_dx=0, pupil_dy=0, closed=False, half_open=False):
    """Draw custom eyes at specified position."""
    cfg = _CUSTOM_EYES_CONFIG
    pr = _get_pupil_r()
    e.draw_rounded_rect_eye(
        cx, cy,
        ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'],
        pupil_dx=pupil_dx, pupil_dy=pupil_dy,
        pupil_r=pr, closed=closed, half_open=half_open
    )


def _draw_custom_mouth(e, x_offset=0, y_offset=0):
    """Draw mouth based on expression, with optional offset."""
    expr = _CUSTOM_EYES_CONFIG['expr']
    mouth_map = {
        'normal': (0, 18, 52),
        'happy': (8, 28, 52),
        'sad': (-6, 22, 52),
        'angry': (-6, 14, 52),
        'surprised': (0, 10, 56),  # O mouth
        'sleepy': (0, 14, 52),
        'wink': (4, 20, 52),
        'love': (10, 26, 52),
        'look_left': (0, 18, 52),
        'look_right': (0, 18, 52),
    }
    smile, width, y_base = mouth_map.get(expr, (0, 18, 52))
    cx = 64 + x_offset  # Mouth center follows eye offset
    if expr == 'surprised':
        e.draw_arc(cx, y_base + y_offset, 7, 0, 360, 1, 2)
    else:
        e.draw_mouth(smile=smile, width=width, y_offset=y_base + y_offset, cx=cx)


def _draw_custom_brow(e, x_offset=0, y_offset=0):
    """Draw eyebrows based on expression, with optional offset."""
    expr = _CUSTOM_EYES_CONFIG['expr']
    cfg = _CUSTOM_EYES_CONFIG
    brow_offset_y = -(cfg['eh'] // 2 + 5) + y_offset
    
    if expr == 'angry':
        e.draw_brow(EYE_L_CX + x_offset, angle_deg=-12, offset_y=brow_offset_y, length=22)
        e.draw_brow(EYE_R_CX + x_offset, angle_deg=12, offset_y=brow_offset_y, length=22)
    elif expr == 'sad':
        e.draw_brow(EYE_L_CX + x_offset, angle_deg=18, offset_y=brow_offset_y, length=22)
        e.draw_brow(EYE_R_CX + x_offset, angle_deg=-18, offset_y=brow_offset_y, length=22)
    elif expr == 'surprised':
        # Raised eyebrows for surprised
        e.draw_brow(EYE_L_CX + x_offset, angle_deg=-8, offset_y=brow_offset_y - 5, length=20)
        e.draw_brow(EYE_R_CX + x_offset, angle_deg=8, offset_y=brow_offset_y - 5, length=20)
    # Other expressions don't need special eyebrows


def _idle_normal(e, frame):
    """Normal idle: random blink."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cfg = _CUSTOM_EYES_CONFIG
    if frame % 100 < 10:  # Blink every ~100 frames
        e.draw_rounded_rect_eye(cx - 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
        e.draw_rounded_rect_eye(cx + 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])


def _idle_happy(e, frame):
    """Happy idle: slight bounce."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    bounce = int(3 * math.sin(2 * math.pi * frame / 30))
    _draw_custom_eyes_at(e, cx - 32, cy + bounce)
    _draw_custom_eyes_at(e, cx + 32, cy + bounce)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'] + bounce)
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'] + bounce)


def _idle_sad(e, frame):
    """Sad idle: looking down, slow blink."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cfg = _CUSTOM_EYES_CONFIG
    if frame % 150 < 15:
        e.draw_rounded_rect_eye(cx - 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
        e.draw_rounded_rect_eye(cx + 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy, pupil_dy=3)
        _draw_custom_eyes_at(e, cx + 32, cy, pupil_dy=3)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])


def _idle_angry(e, frame):
    """Angry idle: slight shake."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    shake = 1 if frame % 20 < 10 else 0
    _draw_custom_eyes_at(e, cx - 32 + shake, cy)
    _draw_custom_eyes_at(e, cx + 32 + shake, cy)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'] + shake, y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])


def _idle_surprised(e, frame):
    """Surprised idle: quick blinks."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cfg = _CUSTOM_EYES_CONFIG
    if frame % 60 < 5:
        e.draw_rounded_rect_eye(cx - 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
        e.draw_rounded_rect_eye(cx + 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])


def _idle_sleepy(e, frame):
    """Sleepy idle: slowly closing eyes."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cycle = frame % 200
    if cycle > 150:
        top_clip = int((cycle - 150) * _CUSTOM_EYES_CONFIG['eh'] / 50)
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
        e.oled.fill_rect(cx - 32 - _CUSTOM_EYES_CONFIG['ew']//2, cy - _CUSTOM_EYES_CONFIG['eh']//2,
                         _CUSTOM_EYES_CONFIG['ew'], top_clip, 0)
        e.oled.fill_rect(cx + 32 - _CUSTOM_EYES_CONFIG['ew']//2, cy - _CUSTOM_EYES_CONFIG['eh']//2,
                         _CUSTOM_EYES_CONFIG['ew'], top_clip, 0)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy, half_open=True)
        _draw_custom_eyes_at(e, cx + 32, cy, half_open=True)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    # Draw zzz - moves with eyes
    for i, (zx, zy) in enumerate([(100, 8), (106, 5), (112, 2)]):
        sz = 2 + i
        e.oled.hline(zx + _CUSTOM_ANIM_STATE['x_offset'], zy + _CUSTOM_ANIM_STATE['y_offset'], sz, 1)
        e.oled.line(zx + sz + _CUSTOM_ANIM_STATE['x_offset'], zy + _CUSTOM_ANIM_STATE['y_offset'],
                    zx + _CUSTOM_ANIM_STATE['x_offset'], zy + sz + _CUSTOM_ANIM_STATE['y_offset'], 1)
        e.oled.hline(zx + _CUSTOM_ANIM_STATE['x_offset'], zy + sz + _CUSTOM_ANIM_STATE['y_offset'], sz, 1)


def _idle_wink(e, frame):
    """Wink idle: occasional wink."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cfg = _CUSTOM_EYES_CONFIG
    if frame % 100 < 20:
        e.draw_rounded_rect_eye(cx - 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'])
        e.draw_rounded_rect_eye(cx + 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])


def _idle_love(e, frame):
    """Love idle: heart pulse."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    pulse = int(2 * math.sin(2 * math.pi * frame / 40))
    _draw_custom_eyes_at(e, cx - 32, cy + pulse)
    _draw_custom_eyes_at(e, cx + 32, cy + pulse)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'] + pulse)
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'] + pulse)


def _idle_look_left(e, frame):
    """Look left idle: pupil stays left + random blink."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cfg = _CUSTOM_EYES_CONFIG
    # Random blink every ~100 frames
    if frame % 100 < 10:
        e.draw_rounded_rect_eye(cx - 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
        e.draw_rounded_rect_eye(cx + 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy, pupil_dx=-5)
        _draw_custom_eyes_at(e, cx + 32, cy, pupil_dx=-5)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])


def _idle_look_right(e, frame):
    """Look right idle: pupil stays right + random blink."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cfg = _CUSTOM_EYES_CONFIG
    # Random blink every ~100 frames
    if frame % 100 < 10:
        e.draw_rounded_rect_eye(cx - 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
        e.draw_rounded_rect_eye(cx + 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy, pupil_dx=5)
        _draw_custom_eyes_at(e, cx + 32, cy, pupil_dx=5)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])


_IDLE_FUNCS = {
    'normal': _idle_normal,
    'happy': _idle_happy,
    'sad': _idle_sad,
    'angry': _idle_angry,
    'surprised': _idle_surprised,
    'sleepy': _idle_sleepy,
    'wink': _idle_wink,
    'love': _idle_love,
    'look_left': _idle_look_left,
    'look_right': _idle_look_right,
}


def _get_move_limits():
    """Calculate safe movement limits based on eye size.

    Screen: 128x64
    Eyes center: x=32/96, y=32
    Mouth: y=52

    Returns:
        (x_max, y_max_up, y_max_down) - maximum offsets in each direction (all ints)
    """
    cfg = _CUSTOM_EYES_CONFIG
    ew, eh = int(cfg['ew']), int(cfg['eh'])

    # X limits: ensure both eyes stay within 0-128
    # Left eye: (32 + x) - ew/2 >= 0  →  x >= -32 + ew/2
    # Right eye: (96 + x) + ew/2 <= 128  →  x <= 32 - ew/2
    x_limit_left = int(-32 + ew // 2 + 2)   # +2 padding
    x_limit_right = int(32 - ew // 2 - 2)

    # Y limits (positive = down, negative = up):
    # Up limit: brow stays >= 0
    #   Brow at: (32 + y) - eh/2 - 8 >= 0  →  y >= eh/2 - 24
    #   So y_min = eh/2 - 24 (negative means can move up)
    y_limit_up = int(-(24 - eh // 2 - 2))  # Can move up by this amount

    # Down limit: mouth stays <= 64
    #   Mouth at: 52 + y <= 60  →  y <= 8
    y_limit_down = 8

    x_max = int(min(abs(x_limit_left), abs(x_limit_right)))

    return x_max, max(0, y_limit_up), y_limit_down


def _update_bounce_position(speed_x=1, speed_y=1):
    """
    Update position with bounce movement.
    Reverses direction when hitting screen limits.

    Args:
        speed_x: horizontal speed (1-3)
        speed_y: vertical speed (1-3)

    Returns:
        (x_offset, y_offset) - new position
    """
    x_max, y_max_up, y_max_down = _get_move_limits()

    # Get current velocity (default to 1 or -1)
    vx = _CUSTOM_ANIM_STATE.get('vx', 1)
    vy = _CUSTOM_ANIM_STATE.get('vy', 1)
    
    # Ensure velocity direction is correct (±1)
    if vx == 0:
        vx = 1
    if vy == 0:
        vy = 1

    # Update position with speed
    x = _CUSTOM_ANIM_STATE['x_offset'] + int(vx * speed_x)
    y = _CUSTOM_ANIM_STATE['y_offset'] + int(vy * speed_y)

    # Bounce off X walls
    if x > x_max:
        x = x_max
        _CUSTOM_ANIM_STATE['vx'] = -abs(vx)
    elif x < -x_max:
        x = -x_max
        _CUSTOM_ANIM_STATE['vx'] = abs(vx)

    # Bounce off Y walls
    if y > y_max_down:
        y = y_max_down
        _CUSTOM_ANIM_STATE['vy'] = -abs(vy)
    elif y < -y_max_up:
        y = -y_max_up
        _CUSTOM_ANIM_STATE['vy'] = abs(vy)

    _CUSTOM_ANIM_STATE['x_offset'] = int(x)
    _CUSTOM_ANIM_STATE['y_offset'] = int(y)

    return x, y


def _move_normal(e, frame, progress):
    """Normal move: bounce around screen."""
    _update_bounce_position(speed_x=1, speed_y=1)
    _idle_normal(e, frame)


def _move_happy(e, frame, progress):
    """Happy move: bounce around with extra bounce."""
    _update_bounce_position(speed_x=2, speed_y=2)
    _idle_happy(e, frame)


def _move_sad(e, frame, progress):
    """Sad move: slow bounce."""
    _update_bounce_position(speed_x=1, speed_y=1)
    _idle_sad(e, frame)


def _move_angry(e, frame, progress):
    """Angry move: fast jerky bounce."""
    _update_bounce_position(speed_x=3, speed_y=2)
    _idle_angry(e, frame)


def _move_surprised(e, frame, progress):
    """Surprised move: quick bounce."""
    _update_bounce_position(speed_x=2, speed_y=3)
    _idle_surprised(e, frame)


def _move_sleepy(e, frame, progress):
    """Sleepy move: very slow bounce."""
    _update_bounce_position(speed_x=1, speed_y=0)
    _idle_sleepy(e, frame)


def _move_wink(e, frame, progress):
    """Wink move: playful fast bounce."""
    _update_bounce_position(speed_x=2, speed_y=2)
    _idle_wink(e, frame)


def _move_love(e, frame, progress):
    """Love move: smooth bounce."""
    _update_bounce_position(speed_x=2, speed_y=2)
    _idle_love(e, frame)


def _move_look_left(e, frame, progress):
    """Look left move: bounce around screen, pupils stay left."""
    _update_bounce_position(speed_x=2, speed_y=2)
    _idle_look_left(e, frame)


def _move_look_right(e, frame, progress):
    """Look right move: bounce around screen, pupils stay right."""
    _update_bounce_position(speed_x=2, speed_y=2)
    _idle_look_right(e, frame)


_MOVE_FUNCS = {
    'normal': _move_normal,
    'happy': _move_happy,
    'sad': _move_sad,
    'angry': _move_angry,
    'surprised': _move_surprised,
    'sleepy': _move_sleepy,
    'wink': _move_wink,
    'love': _move_love,
    'look_left': _move_look_left,
    'look_right': _move_look_right,
}


def _action_normal(e, frame):
    """Normal action: look around."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    look_seq = [0, -5, 0, 5, 0]
    idx = min(frame // 20, len(look_seq) - 1)
    dx = look_seq[idx]
    _draw_custom_eyes_at(e, cx - 32, cy, pupil_dx=dx)
    _draw_custom_eyes_at(e, cx + 32, cy, pupil_dx=dx)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    return idx >= len(look_seq) - 1


def _action_happy(e, frame):
    """Happy action: big smile bounce."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    bounce = int(5 * math.sin(2 * math.pi * frame / 15))
    _draw_custom_eyes_at(e, cx - 32, cy + bounce)
    _draw_custom_eyes_at(e, cx + 32, cy + bounce)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'] + bounce)
    # Extra wide smile - mouth follows bounce
    e.draw_mouth(smile=12, width=32, y_offset=52 + _CUSTOM_ANIM_STATE['y_offset'] + bounce, cx=64 + _CUSTOM_ANIM_STATE['x_offset'])
    return frame >= 45


def _action_sad(e, frame):
    """Sad action: slow close and open."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    if frame < 30:
        top_clip = int(frame * _CUSTOM_EYES_CONFIG['eh'] / 30)
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
        e.oled.fill_rect(cx - 32 - _CUSTOM_EYES_CONFIG['ew']//2, cy - _CUSTOM_EYES_CONFIG['eh']//2,
                         _CUSTOM_EYES_CONFIG['ew'], top_clip, 0)
        e.oled.fill_rect(cx + 32 - _CUSTOM_EYES_CONFIG['ew']//2, cy - _CUSTOM_EYES_CONFIG['eh']//2,
                         _CUSTOM_EYES_CONFIG['ew'], top_clip, 0)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    return frame >= 60


def _action_angry(e, frame):
    """Angry action: intense shake."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    shake_x = 3 * (1 if frame % 10 < 5 else -1)
    shake_y = 2 * (1 if frame % 8 < 4 else -1)
    _draw_custom_eyes_at(e, cx - 32 + shake_x, cy + shake_y, pupil_dy=2)
    _draw_custom_eyes_at(e, cx + 32 + shake_x, cy + shake_y, pupil_dy=2)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'] + shake_x, y_offset=_CUSTOM_ANIM_STATE['y_offset'] + shake_y)
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'] + shake_x, y_offset=_CUSTOM_ANIM_STATE['y_offset'] + shake_y)
    return frame >= 40


def _action_surprised(e, frame):
    """Surprised action: jump and shake."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    if frame < 20:
        y = -int(10 * math.sin(math.pi * frame / 20))
        shake = 2 * (1 if frame % 6 < 3 else -1)
        _draw_custom_eyes_at(e, cx - 32 + shake, cy + y)
        _draw_custom_eyes_at(e, cx + 32 + shake, cy + y)
        _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'] + shake, y_offset=_CUSTOM_ANIM_STATE['y_offset'] + y)
        _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'] + shake, y_offset=_CUSTOM_ANIM_STATE['y_offset'] + y)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
        _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
        _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    return frame >= 40


def _action_sleepy(e, frame):
    """Sleepy action: fully close then wake."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cfg = _CUSTOM_EYES_CONFIG
    if frame < 40:
        e.draw_rounded_rect_eye(cx - 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
        e.draw_rounded_rect_eye(cx + 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
    elif frame < 80:
        open_pct = (frame - 40) / 40
        top_clip = int((1 - open_pct) * cfg['eh'])
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
        e.oled.fill_rect(cx - 32 - cfg['ew']//2, cy - cfg['eh']//2,
                         cfg['ew'], top_clip, 0)
        e.oled.fill_rect(cx + 32 - cfg['ew']//2, cy - cfg['eh']//2,
                         cfg['ew'], top_clip, 0)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy, half_open=True)
        _draw_custom_eyes_at(e, cx + 32, cy, half_open=True)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    # zzz - moves with eyes
    for i, (zx, zy) in enumerate([(100, 8), (106, 5), (112, 2)]):
        sz = 2 + i
        e.oled.hline(zx + _CUSTOM_ANIM_STATE['x_offset'], zy + _CUSTOM_ANIM_STATE['y_offset'], sz, 1)
        e.oled.line(zx + sz + _CUSTOM_ANIM_STATE['x_offset'], zy + _CUSTOM_ANIM_STATE['y_offset'],
                    zx + _CUSTOM_ANIM_STATE['x_offset'], zy + sz + _CUSTOM_ANIM_STATE['y_offset'], 1)
        e.oled.hline(zx + _CUSTOM_ANIM_STATE['x_offset'], zy + sz + _CUSTOM_ANIM_STATE['y_offset'], sz, 1)
    return frame >= 100


def _action_wink(e, frame):
    """Wink action: double wink."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    cfg = _CUSTOM_EYES_CONFIG
    wink = (frame // 20) % 2 == 0
    if wink:
        e.draw_rounded_rect_eye(cx - 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'])
        e.draw_rounded_rect_eye(cx + 32, cy, ew=cfg['ew'], eh=cfg['eh'], rx=cfg['rx'], closed=True)
    else:
        _draw_custom_eyes_at(e, cx - 32, cy)
        _draw_custom_eyes_at(e, cx + 32, cy)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    return frame >= 60


def _action_love(e, frame):
    """Love action: hearts float up."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    pulse = int(3 * math.sin(2 * math.pi * frame / 30))
    _draw_custom_eyes_at(e, cx - 32, cy + pulse)
    _draw_custom_eyes_at(e, cx + 32, cy + pulse)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'] + pulse)
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'] + pulse)
    # Draw floating hearts - clamp to screen
    heart_y = max(4, min(44, cy - 20 - (frame * 2) % 40 + _CUSTOM_ANIM_STATE['y_offset']))
    if frame % 30 < 20:
        e.oled.pixel(cx + 10, heart_y, 1)
        e.oled.pixel(cx + 11, heart_y, 1)
        e.oled.pixel(cx + 9, heart_y + 1, 1)
        e.oled.pixel(cx + 12, heart_y + 1, 1)
        e.oled.pixel(cx + 8, heart_y + 2, 1)
        e.oled.pixel(cx + 13, heart_y + 2, 1)
        e.oled.pixel(cx + 10, heart_y + 3, 1)
        e.oled.pixel(cx + 11, heart_y + 3, 1)
    return frame >= 90


def _action_look_left(e, frame):
    """Look left action: glance left then center."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    if frame < 20:
        dx = -8
    elif frame < 40:
        dx = -4
    else:
        dx = 0
    _draw_custom_eyes_at(e, cx - 32, cy, pupil_dx=dx)
    _draw_custom_eyes_at(e, cx + 32, cy, pupil_dx=dx)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    return frame >= 50


def _action_look_right(e, frame):
    """Look right action: glance right then center."""
    cx, cy = 64 + _CUSTOM_ANIM_STATE['x_offset'], 32 + _CUSTOM_ANIM_STATE['y_offset']
    if frame < 20:
        dx = 8
    elif frame < 40:
        dx = 4
    else:
        dx = 0
    _draw_custom_eyes_at(e, cx - 32, cy, pupil_dx=dx)
    _draw_custom_eyes_at(e, cx + 32, cy, pupil_dx=dx)
    _draw_custom_brow(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    _draw_custom_mouth(e, x_offset=_CUSTOM_ANIM_STATE['x_offset'], y_offset=_CUSTOM_ANIM_STATE['y_offset'])
    return frame >= 50


_ACTION_FUNCS = {
    'normal': _action_normal,
    'happy': _action_happy,
    'sad': _action_sad,
    'angry': _action_angry,
    'surprised': _action_surprised,
    'sleepy': _action_sleepy,
    'wink': _action_wink,
    'love': _action_love,
    'look_left': _action_look_left,
    'look_right': _action_look_right,
}


def animate_custom_eyes(e, mode='all'):
    """
    NON-BLOCKING: Animate custom eyes based on expression.
    Call repeatedly in 'while True' loop with small delay (e.g., time.sleep_ms(50)).
    
    Args:
        e: Eyes instance
        mode: 'idle' | 'move' | 'action' | 'all'
            - idle: Stay in place with expression-specific idle animation
            - move: Travel around screen with expression-specific movement
            - action: Perform expression-specific special action
            - all: Cycle through idle (2s) → move (3s) → action → repeat
    
    Example:
        # In init():
        set_custom_eyes_config(expr='angry', ew=40, eh=40, rx=10, pupil='medium')
        
        # In while True:
        animate_custom_eyes(e, mode='all')
        time.sleep_ms(50)  # Adjust for desired framerate
    """
    global _CUSTOM_ANIM_STATE
    
    now = time.ticks_ms()
    expr = _CUSTOM_EYES_CONFIG['expr']
    
    # Get animation functions for current expression
    idle_fn = _IDLE_FUNCS.get(expr, _idle_normal)
    move_fn = _MOVE_FUNCS.get(expr, _move_normal)
    action_fn = _ACTION_FUNCS.get(expr, _action_normal)
    
    # Handle mode switching for 'all' mode
    if mode == 'all':
        elapsed = time.ticks_diff(now, _CUSTOM_ANIM_STATE['last_switch'])

        if _CUSTOM_ANIM_STATE['phase'] == 'idle' and elapsed >= _CUSTOM_ANIM_STATE['idle_duration']:
            _CUSTOM_ANIM_STATE['phase'] = 'move'
            _CUSTOM_ANIM_STATE['last_switch'] = now
            _CUSTOM_ANIM_STATE['frame'] = 0
        elif _CUSTOM_ANIM_STATE['phase'] == 'move' and elapsed >= _CUSTOM_ANIM_STATE['move_duration']:
            _CUSTOM_ANIM_STATE['phase'] = 'action'
            _CUSTOM_ANIM_STATE['last_switch'] = now
            _CUSTOM_ANIM_STATE['frame'] = 0
            _CUSTOM_ANIM_STATE['action_frame'] = 0
        elif _CUSTOM_ANIM_STATE['phase'] == 'action':
            _CUSTOM_ANIM_STATE['action_frame'] += 1
            if _CUSTOM_ANIM_STATE['action_frame'] >= 60:  # Default action duration
                _CUSTOM_ANIM_STATE['phase'] = 'idle'
                _CUSTOM_ANIM_STATE['last_switch'] = now
                _CUSTOM_ANIM_STATE['frame'] = 0
                _CUSTOM_ANIM_STATE['action_frame'] = 0
    else:
        # Standalone mode: idle, move, or action
        _CUSTOM_ANIM_STATE['phase'] = mode
        _CUSTOM_ANIM_STATE['last_switch'] = now
        # Increment action_frame for standalone action mode
        if mode == 'action':
            _CUSTOM_ANIM_STATE['action_frame'] += 1
            if _CUSTOM_ANIM_STATE['action_frame'] >= 60:
                _CUSTOM_ANIM_STATE['action_frame'] = 0  # Loop action
    
    # Clear screen
    e.clear()
    
    # Increment frame counter
    _CUSTOM_ANIM_STATE['frame'] += 1
    frame = _CUSTOM_ANIM_STATE['frame']
    progress = (frame % 300) / 300.0  # 0-1 cycle for move animations
    
    # Render based on current phase
    phase = _CUSTOM_ANIM_STATE['phase']
    
    if phase == 'idle':
        idle_fn(e, frame)
    elif phase == 'move':
        move_fn(e, frame, progress)
    elif phase == 'action':
        action_fn(e, _CUSTOM_ANIM_STATE['action_frame'])
    
    e.show()
    gc.collect()

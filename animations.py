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

def _draw_mouth_on(e, smile=0, width=18):
    e.draw_mouth(smile=smile, width=width)

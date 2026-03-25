# expressions.py — Robot facial expression library
# Requires: eyes.py (Eyes class)
# Each expression is a function: expr_name(e: Eyes) -> None

from eyes import Eyes, EYE_L_CX, EYE_R_CX, EYE_CY, EYE_W, EYE_H
import math


# ================================================================== #
#  EXPRESSION DEFINITIONS                                             #
# ================================================================== #

def expr_normal(e: Eyes):
    """Default resting face — round open eyes, neutral mouth."""
    e.draw_both_eyes(ew=EYE_W, eh=EYE_H)
    e.draw_mouth(smile=0, width=18)


def expr_happy(e: Eyes):
    """
    Happy — eyes curve upward (arc), big smile.
    Eyes drawn as upward-opening arcs (white filled bottom half).
    """
    for cx in (EYE_L_CX, EYE_R_CX):
        # Draw arc eyes (happy squint = lower half ellipse)
        e.draw_eye(cx, EYE_CY, ew=EYE_W, eh=EYE_H, half_open=False)
        # Overwrite top half with black (creates arc-eye effect)
        e.clip_rect(cx - EYE_W // 2 - 1, EYE_CY - EYE_H // 2 - 1,
                    EYE_W + 2, EYE_H // 2, 0)
        # Draw arc outline on top
        e.draw_arc(cx, EYE_CY + 2, EYE_W // 2 - 1, 190, 350, 1, 2)
    e.draw_mouth(smile=8, width=28)


def expr_sad(e: Eyes):
    """Sad — inner corners of eyebrows pushed down, drooping mouth."""
    e.draw_eye(EYE_L_CX, EYE_CY, ew=EYE_W, eh=EYE_H, top_clip=8)
    e.draw_eye(EYE_R_CX, EYE_CY, ew=EYE_W, eh=EYE_H, top_clip=8)
    # Sad brows — slanted inward (inner brow lower)
    e.draw_brow(EYE_L_CX, angle_deg=18,  offset_y=-17, length=22)
    e.draw_brow(EYE_R_CX, angle_deg=-18, offset_y=-17, length=22)
    # Downward mouth
    e.draw_mouth(smile=-6, width=22)


def expr_angry(e: Eyes):
    """Angry — outer corners of eyebrows pushed down, glaring eyes."""
    e.draw_eye(EYE_L_CX, EYE_CY, ew=EYE_W, eh=EYE_H,
               top_clip=9, pupil_dy=3)
    e.draw_eye(EYE_R_CX, EYE_CY, ew=EYE_W, eh=EYE_H,
               top_clip=9, pupil_dy=3)
    # Angry eyebrows — outer ends lower
    e.draw_brow(EYE_L_CX, angle_deg=-12, offset_y=-17, length=22)
    e.draw_brow(EYE_R_CX, angle_deg=12,  offset_y=-17, length=22)
    # Tight mouth
    e.draw_mouth(smile=0, width=14)


def expr_surprised(e: Eyes):
    """Surprised — very wide eyes, open O mouth."""
    e.draw_both_eyes(ew=EYE_W + 6, eh=EYE_H + 6)
    # O-shaped mouth
    e.draw_arc(64, 56, 7, 0, 360, 1, 2)


def expr_sleepy(e: Eyes):
    """Sleepy — half-open eyes, zzz text."""
    e.draw_eye(EYE_L_CX, EYE_CY, ew=EYE_W, eh=EYE_H, half_open=True)
    e.draw_eye(EYE_R_CX, EYE_CY, ew=EYE_W, eh=EYE_H, half_open=True)
    # "zzz" using small pixel font
    for i, (zx, zy) in enumerate([(100, 8), (106, 5), (112, 2)]):
        s = 2 + i
        # Draw a tiny Z shape
        e.oled.hline(zx,     zy,     s, 1)
        e.oled.line( zx + s, zy,     zx,     zy + s, 1)
        e.oled.hline(zx,     zy + s, s, 1)


def expr_confused(e: Eyes):
    """Confused — one normal eye, one raised eyebrow, wavy mouth."""
    e.draw_eye(EYE_L_CX, EYE_CY, ew=EYE_W, eh=EYE_H)
    e.draw_eye(EYE_R_CX, EYE_CY, ew=EYE_W, eh=EYE_H,
               pupil_dx=3, pupil_dy=-3)
    # One eyebrow raised
    e.draw_brow(EYE_R_CX, angle_deg=-8, offset_y=-22, length=20)
    # Wavy mouth (approximate with segments)
    cx = 64
    for i in range(4):
        x1 = cx - 12 + i * 6
        x2 = x1 + 6
        y1 = 54 + (0 if i % 2 == 0 else 3)
        y2 = 54 + (3 if i % 2 == 0 else 0)
        e.oled.line(x1, y1, x2, y2, 1)


def expr_love(e: Eyes):
    """Love — heart-shaped eyes."""
    for cx in (EYE_L_CX, EYE_R_CX):
        _draw_heart(e, cx, EYE_CY, size=10)
    e.draw_mouth(smile=10, width=26)


def _draw_heart(e: Eyes, cx, cy, size=10):
    """Draw a pixelated heart shape."""
    s = size // 2
    for dy in range(-s, s + 1):
        for dx in range(-s - 1, s + 2):
            # Heart formula: (x²+y²-1)³ - x²y³ ≤ 0
            # Normalised to [-1,1] range
            nx = dx / (s + 1)
            ny = -dy / s   # flip Y for display
            val = (nx**2 + ny**2 - 1)**3 - nx**2 * ny**3
            if val <= 0:
                px = cx + dx
                py = cy + dy
                if 0 <= px < 128 and 0 <= py < 64:
                    e.oled.pixel(px, py, 1)


def expr_blink(e: Eyes):
    """Mid-blink frame — both eyes closed."""
    e.draw_eye(EYE_L_CX, EYE_CY, closed=True)
    e.draw_eye(EYE_R_CX, EYE_CY, closed=True)
    e.draw_mouth(smile=0, width=18)


def expr_look_left(e: Eyes):
    """Looking left — pupils shifted left."""
    e.draw_both_eyes(ew=EYE_W, eh=EYE_H, pupil_dx=-5)
    e.draw_mouth(smile=0, width=18)


def expr_look_right(e: Eyes):
    """Looking right — pupils shifted right."""
    e.draw_both_eyes(ew=EYE_W, eh=EYE_H, pupil_dx=5)
    e.draw_mouth(smile=0, width=18)


def expr_wink(e: Eyes):
    """Wink — right eye closed, left normal."""
    e.draw_eye(EYE_L_CX, EYE_CY, ew=EYE_W, eh=EYE_H)
    e.draw_eye(EYE_R_CX, EYE_CY, closed=True)
    e.draw_mouth(smile=4, width=20)


# ================================================================== #
#  EXPRESSION REGISTRY                                                #
# ================================================================== #

EXPRESSIONS = {
    "normal":    expr_normal,
    "happy":     expr_happy,
    "sad":       expr_sad,
    "angry":     expr_angry,
    "surprised": expr_surprised,
    "sleepy":    expr_sleepy,
    "confused":  expr_confused,
    "love":      expr_love,
    "blink":     expr_blink,
    "look_left": expr_look_left,
    "look_right":expr_look_right,
    "wink":      expr_wink,
}


def show_expression(eyes: Eyes, name: str):
    """
    Show a named expression.
    Example: show_expression(e, "happy")
    """
    fn = EXPRESSIONS.get(name)
    if fn is None:
        raise ValueError("Unknown expression: {}".format(name))
    eyes.clear()
    fn(eyes)
    eyes.show()

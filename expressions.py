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
    # Tight mouth - upward curved (suppressed anger)
    e.draw_mouth(smile=-6, width=14)


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
#  STYLE A — ROUNDED RECTANGLE EXPRESSIONS                           #
#  shape: "sharp" rx=4 | "balanced" rx=10 | "round" rx=18 | "wide"  #
# ================================================================== #

SQUARE_SHAPES = {
    "sharp":    {"ew": 28, "eh": 28, "rx": 4},
    "balanced": {"ew": 28, "eh": 28, "rx": 10},
    "round":    {"ew": 28, "eh": 28, "rx": 14},
    "wide":     {"ew": 36, "eh": 22, "rx": 8},
}

def _sq(shape):
    """Return shape kwargs for square style, defaulting to balanced."""
    return SQUARE_SHAPES.get(shape, SQUARE_SHAPES["balanced"])

def expr_square_normal(e, shape="balanced"):
    s = _sq(shape)
    e.draw_both_rounded_rect_eyes(**s)
    e.draw_mouth(smile=0, width=18)

def expr_square_happy(e, shape="balanced"):
    s = _sq(shape)
    for cx in (EYE_L_CX, EYE_R_CX):
        e.draw_rounded_rect_eye(cx, EYE_CY, **s)
        e.clip_rect(cx - s["ew"]//2 - 1, EYE_CY - s["eh"]//2 - 1,
                    s["ew"] + 2, s["eh"]//2, 0)
        e.draw_arc(cx, EYE_CY + 2, s["ew"]//2 - 1, 190, 350, 1, 2)
    e.draw_mouth(smile=8, width=28)

def expr_square_sad(e, shape="balanced"):
    s = _sq(shape)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY, top_angle_right=s["eh"]//3, **s)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY, top_angle_left=s["eh"]//3, **s)
    e.draw_brow(EYE_L_CX, angle_deg=18,  offset_y=-17, length=22)
    e.draw_brow(EYE_R_CX, angle_deg=-18, offset_y=-17, length=22)
    e.draw_mouth(smile=-6, width=22)

def expr_square_angry(e, shape="balanced"):
    s = _sq(shape)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY, top_angle_left=s["eh"]//3, **s)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY, top_angle_right=s["eh"]//3, **s)
    e.draw_brow(EYE_L_CX, angle_deg=-12, offset_y=-17, length=22)
    e.draw_brow(EYE_R_CX, angle_deg=12,  offset_y=-17, length=22)
    # Tight mouth - upward curved (suppressed anger)
    e.draw_mouth(smile=-6, width=14)

def expr_square_surprised(e, shape="balanced"):
    s = _sq(shape)
    e.draw_both_rounded_rect_eyes(
        ew=s["ew"] + 6, eh=s["eh"] + 8, rx=s["rx"])
    e.draw_arc(64, 56, 7, 0, 360, 1, 2)

def expr_square_sleepy(e, shape="balanced"):
    s = _sq(shape)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY, half_open=True, **s)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY, half_open=True, **s)
    for i, (zx, zy) in enumerate([(100, 8), (106, 5), (112, 2)]):
        sz = 2 + i
        e.oled.hline(zx,      zy,      sz, 1)
        e.oled.line( zx + sz, zy,      zx,      zy + sz, 1)
        e.oled.hline(zx,      zy + sz, sz, 1)

def expr_square_wink(e, shape="balanced"):
    s = _sq(shape)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY, **s)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY, closed=True, **s)
    e.draw_mouth(smile=4, width=20)

def expr_square_love(e, shape="balanced"):
    s = _sq(shape)
    for cx in (EYE_L_CX, EYE_R_CX):
        e.draw_rounded_rect_eye(cx, EYE_CY, **s)
        # Clear interior then draw heart
        e.clip_rect(cx - s["ew"]//2 + 2, EYE_CY - s["eh"]//2 + 2,
                    s["ew"] - 4, s["eh"] - 4, 0)
        _draw_heart(e, cx, EYE_CY, size=min(s["ew"], s["eh"]) - 6)
    e.draw_mouth(smile=10, width=26)

def expr_square_look_left(e, shape="balanced"):
    s = _sq(shape)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY, pupil_dx=-5, **s)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY, pupil_dx=-5, **s)
    e.draw_mouth(smile=0, width=18)

def expr_square_look_right(e, shape="balanced"):
    s = _sq(shape)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY, pupil_dx=5, **s)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY, pupil_dx=5, **s)
    e.draw_mouth(smile=0, width=18)


SQUARE_EXPRESSIONS = {
    "normal":    expr_square_normal,
    "happy":     expr_square_happy,
    "sad":       expr_square_sad,
    "angry":     expr_square_angry,
    "surprised": expr_square_surprised,
    "sleepy":    expr_square_sleepy,
    "wink":      expr_square_wink,
    "love":      expr_square_love,
    "look_left": expr_square_look_left,
    "look_right": expr_square_look_right,
}

def show_square_expression(eyes, shape="balanced", expr="normal"):
    """
    Show Style A rounded-rectangle expression.
    shape: "sharp" | "balanced" | "round" | "wide"
    expr:  "normal" | "happy" | "sad" | "angry" | "surprised" | "sleepy" | "wink" | "love"
    """
    fn = SQUARE_EXPRESSIONS.get(expr)
    if fn is None:
        raise ValueError("Unknown square expression: {}".format(expr))
    eyes.clear()
    fn(eyes, shape=shape)
    eyes.show()


# ================================================================== #
#  STYLE B — OGGY OVAL EXPRESSIONS                                   #
#  shape: "normal" | "wide" | "tall" | "big"                         #
# ================================================================== #

OVAL_SHAPES = {
    "normal": {"outer_rx": 26, "outer_ry": 20, "inner_rx": 16, "inner_ry": 13},
    "wide":   {"outer_rx": 30, "outer_ry": 14, "inner_rx": 20, "inner_ry":  9},
    "tall":   {"outer_rx": 22, "outer_ry": 28, "inner_rx": 15, "inner_ry": 22},
    "big":    {"outer_rx": 28, "outer_ry": 26, "inner_rx": 19, "inner_ry": 20},
}

def _ov(shape):
    """Return shape kwargs for oval style, defaulting to normal."""
    return OVAL_SHAPES.get(shape, OVAL_SHAPES["normal"])

def expr_oval_normal(e, shape="normal"):
    s = _ov(shape)
    e.draw_both_oval_eyes(**s)
    e.draw_mouth(smile=0, width=18)

def expr_oval_happy(e, shape="normal"):
    s = _ov(shape)
    for cx in (EYE_L_CX, EYE_R_CX):
        e.draw_oval_eye(cx, EYE_CY, **s)
        e.oled.fill_rect(cx - s["outer_rx"] - 1, EYE_CY - s["outer_ry"] - 1,
                         s["outer_rx"] * 2 + 2, s["outer_ry"], 0)
        e.draw_arc(cx, EYE_CY + 2, s["outer_rx"] - 2, 190, 350, 1, 2)
    e.draw_mouth(smile=8, width=28)

def expr_oval_sad(e, shape="normal"):
    s = _ov(shape)
    clip = s["outer_ry"] // 3
    e.draw_oval_eye(EYE_L_CX, EYE_CY, top_angle_right=clip, **s)
    e.draw_oval_eye(EYE_R_CX, EYE_CY, top_angle_left=clip,  **s)
    e.draw_brow(EYE_L_CX, angle_deg=18,  offset_y=-s["outer_ry"] - 4, length=22)
    e.draw_brow(EYE_R_CX, angle_deg=-18, offset_y=-s["outer_ry"] - 4, length=22)
    e.draw_mouth(smile=-6, width=22)

def expr_oval_angry(e, shape="normal"):
    s = _ov(shape)
    clip = s["outer_ry"] // 2
    e.draw_oval_eye(EYE_L_CX, EYE_CY, top_angle_left=clip,  **s)
    e.draw_oval_eye(EYE_R_CX, EYE_CY, top_angle_right=clip, **s)
    e.draw_brow(EYE_L_CX, angle_deg=-12, offset_y=-s["outer_ry"] - 4, length=24)
    e.draw_brow(EYE_R_CX, angle_deg=12,  offset_y=-s["outer_ry"] - 4, length=24)
    # Tight mouth - upward curved (suppressed anger)
    e.draw_mouth(smile=-6, width=14)

def expr_oval_surprised(e, shape="normal"):
    s = _ov(shape)
    e.draw_both_oval_eyes(
        outer_rx=s["outer_rx"] + 4, outer_ry=s["outer_ry"] + 6,
        inner_rx=s["inner_rx"] + 3, inner_ry=s["inner_ry"] + 5)
    e.draw_arc(64, 56, 7, 0, 360, 1, 2)

def expr_oval_sleepy(e, shape="normal"):
    s = _ov(shape)
    e.draw_oval_eye(EYE_L_CX, EYE_CY, half_open=True, **s)
    e.draw_oval_eye(EYE_R_CX, EYE_CY, half_open=True, **s)
    for i, (zx, zy) in enumerate([(100, 8), (106, 5), (112, 2)]):
        sz = 2 + i
        e.oled.hline(zx,      zy,      sz, 1)
        e.oled.line( zx + sz, zy,      zx,      zy + sz, 1)
        e.oled.hline(zx,      zy + sz, sz, 1)

def expr_oval_wink(e, shape="normal"):
    s = _ov(shape)
    e.draw_oval_eye(EYE_L_CX, EYE_CY, **s)
    e.draw_oval_eye(EYE_R_CX, EYE_CY, closed=True, **s)
    e.draw_mouth(smile=4, width=20)

def expr_oval_love(e, shape="normal"):
    s = _ov(shape)
    for cx in (EYE_L_CX, EYE_R_CX):
        e.draw_oval_eye(cx, EYE_CY, **s)
        e.draw_filled_ellipse(cx, EYE_CY, s["inner_rx"] - 1, s["inner_ry"] - 1, 0)
        _draw_heart(e, cx, EYE_CY, size=min(s["inner_rx"], s["inner_ry"]) * 2 - 4)
    e.draw_mouth(smile=10, width=26)

def expr_oval_look_left(e, shape="normal"):
    s = _ov(shape)
    e.draw_oval_eye(EYE_L_CX, EYE_CY, pupil_dx=-5, **s)
    e.draw_oval_eye(EYE_R_CX, EYE_CY, pupil_dx=-5, **s)
    e.draw_mouth(smile=0, width=18)

def expr_oval_look_right(e, shape="normal"):
    s = _ov(shape)
    e.draw_oval_eye(EYE_L_CX, EYE_CY, pupil_dx=5, **s)
    e.draw_oval_eye(EYE_R_CX, EYE_CY, pupil_dx=5, **s)
    e.draw_mouth(smile=0, width=18)


OVAL_EXPRESSIONS = {
    "normal":    expr_oval_normal,
    "happy":     expr_oval_happy,
    "sad":       expr_oval_sad,
    "angry":     expr_oval_angry,
    "surprised": expr_oval_surprised,
    "sleepy":    expr_oval_sleepy,
    "wink":      expr_oval_wink,
    "love":      expr_oval_love,
    "look_left": expr_oval_look_left,
    "look_right": expr_oval_look_right,
}

def show_oval_expression(eyes, shape="normal", expr="normal"):
    """
    Show Style B Oggy-oval expression.
    shape: "normal" | "wide" | "tall" | "big"
    expr:  "normal" | "happy" | "sad" | "angry" | "surprised" | "sleepy" | "wink" | "love"
    """
    fn = OVAL_EXPRESSIONS.get(expr)
    if fn is None:
        raise ValueError("Unknown oval expression: {}".format(expr))
    eyes.clear()
    fn(eyes, shape=shape)
    eyes.show()


# ================================================================== #
#  STYLE C — CUSTOM SHAPE EXPRESSIONS                                 #
#  Người dùng tự nhập: ew, eh, rx, và kích thước con ngươi           #
#                                                                      #
#  Giới hạn an toàn (màn hình 128x64):                                #
#    ew : 10 – 56 px  (2 mắt tại x=32/96, gap tối thiểu 4px/bên)    #
#    eh : 10 – 40 px  (tâm y=32, miệng y=52, buffer 8px)             #
#    rx : 0 – min(ew,eh)//2  (tự động clamp)                         #
# ================================================================== #

CUSTOM_EW_MIN = 10
CUSTOM_EW_MAX = 56
CUSTOM_EH_MIN = 10
CUSTOM_EH_MAX = 40


def _validate_custom_params(ew, eh, rx):
    """Clamp ew/eh/rx về vùng an toàn, trả về (ew, eh, rx) đã hợp lệ."""
    ew = max(CUSTOM_EW_MIN, min(CUSTOM_EW_MAX, int(ew)))
    eh = max(CUSTOM_EH_MIN, min(CUSTOM_EH_MAX, int(eh)))
    rx_max = min(ew, eh) // 2
    rx = max(0, min(rx_max, int(rx)))
    return ew, eh, rx


def _pupil_r_for(es, pupil_size="medium"):
    """
    Tính bán kính con ngươi theo chiều rộng mắt và lựa chọn người dùng.
    Công thức tỷ lệ với ew, có floor để không bị mất khi mắt nhỏ.
    """
    if pupil_size == "small":
        return max(4, es // 5)
    elif pupil_size == "large":
        return max(6, es // 3)
    else:  # "medium"
        return max(5, es // 4)


def expr_custom_normal(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    pr = _pupil_r_for(min(ew, eh), pupil_size)
    e.draw_both_rounded_rect_eyes(ew=ew, eh=eh, rx=rx, pupil_r=pr)
    e.draw_mouth(smile=0, width=18)


def expr_custom_happy(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    # Happy: xoá nửa trên mắt tạo hiệu ứng mắt cười — con ngươi không hiển thị
    for cx in (EYE_L_CX, EYE_R_CX):
        e.draw_rounded_rect_eye(cx, EYE_CY, ew=ew, eh=eh, rx=rx)
        e.clip_rect(cx - ew // 2 - 1, EYE_CY - eh // 2 - 1,
                    ew + 2, eh // 2, 0)
        e.draw_arc(cx, EYE_CY + 2, ew // 2 - 1, 190, 350, 1, 2)
    e.draw_mouth(smile=8, width=28)


def expr_custom_sad(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    pr = _pupil_r_for(min(ew, eh), pupil_size)
    top_clip = max(2, eh // 4)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY,
                             ew=ew, eh=eh, rx=rx,
                             top_angle_right=top_clip, pupil_r=pr)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY,
                             ew=ew, eh=eh, rx=rx,
                             top_angle_left=top_clip, pupil_r=pr)
    brow_offset = -(eh // 2 + 5)
    e.draw_brow(EYE_L_CX, angle_deg=18,  offset_y=brow_offset, length=22)
    e.draw_brow(EYE_R_CX, angle_deg=-18, offset_y=brow_offset, length=22)
    e.draw_mouth(smile=-6, width=22)


def expr_custom_angry(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    pr = _pupil_r_for(min(ew, eh), pupil_size)
    top_clip = max(2, eh // 3)
    pupil_down = max(2, eh // 8)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY,
                             ew=ew, eh=eh, rx=rx,
                             top_angle_left=top_clip,
                             pupil_dy=pupil_down, pupil_r=pr)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY,
                             ew=ew, eh=eh, rx=rx,
                             top_angle_right=top_clip,
                             pupil_dy=pupil_down, pupil_r=pr)
    brow_offset = -(eh // 2 + 5)
    e.draw_brow(EYE_L_CX, angle_deg=-12, offset_y=brow_offset, length=22)
    e.draw_brow(EYE_R_CX, angle_deg=12,  offset_y=brow_offset, length=22)
    e.draw_mouth(smile=-6, width=14)


def expr_custom_surprised(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    pr = _pupil_r_for(min(ew, eh), pupil_size)
    ew2 = min(CUSTOM_EW_MAX, ew + 6)
    eh2 = min(CUSTOM_EH_MAX, eh + 8)
    e.draw_both_rounded_rect_eyes(ew=ew2, eh=eh2, rx=rx, pupil_r=pr)
    e.draw_arc(64, 56, 7, 0, 360, 1, 2)


def expr_custom_sleepy(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    pr = _pupil_r_for(min(ew, eh), pupil_size)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY,
                             ew=ew, eh=eh, rx=rx, half_open=True, pupil_r=pr)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY,
                             ew=ew, eh=eh, rx=rx, half_open=True, pupil_r=pr)
    for i, (zx, zy) in enumerate([(100, 8), (106, 5), (112, 2)]):
        sz = 2 + i
        e.oled.hline(zx,      zy,      sz, 1)
        e.oled.line( zx + sz, zy,      zx,      zy + sz, 1)
        e.oled.hline(zx,      zy + sz, sz, 1)


def expr_custom_wink(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    pr = _pupil_r_for(min(ew, eh), pupil_size)
    e.draw_rounded_rect_eye(EYE_L_CX, EYE_CY,
                             ew=ew, eh=eh, rx=rx, pupil_r=pr)
    e.draw_rounded_rect_eye(EYE_R_CX, EYE_CY,
                             ew=ew, eh=eh, rx=rx, closed=True)
    e.draw_mouth(smile=4, width=20)


def expr_custom_love(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    # Love: trái tim thay con ngươi — kích thước tim phụ thuộc pupil_size
    base_size = max(6, min(ew, eh) - 6)
    
    # Tính kích thước tim theo pupil_size
    if pupil_size == "small":
        heart_size = int(max(4, base_size * 0.6))
    elif pupil_size == "large":
        heart_size = int(max(8, base_size * 1.0))
    else:  # medium
        heart_size = int(max(6, base_size * 0.8))
    
    for cx in (EYE_L_CX, EYE_R_CX):
        e.draw_rounded_rect_eye(cx, EYE_CY, ew=ew, eh=eh, rx=rx)
        e.clip_rect(cx - ew // 2 + 2, EYE_CY - eh // 2 + 2,
                    ew - 4, eh - 4, 0)
        _draw_heart(e, cx, EYE_CY, size=heart_size)
    e.draw_mouth(smile=10, width=26)


def expr_custom_look_left(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    pr = _pupil_r_for(min(ew, eh), pupil_size)
    dx = max(3, ew // 6)
    e.draw_both_rounded_rect_eyes(ew=ew, eh=eh, rx=rx,
                                   pupil_dx=-dx, pupil_r=pr)
    e.draw_mouth(smile=0, width=18)


def expr_custom_look_right(e, ew=28, eh=28, rx=10, pupil_size="medium"):
    pr = _pupil_r_for(min(ew, eh), pupil_size)
    dx = max(3, ew // 6)
    e.draw_both_rounded_rect_eyes(ew=ew, eh=eh, rx=rx,
                                   pupil_dx=dx, pupil_r=pr)
    e.draw_mouth(smile=0, width=18)


CUSTOM_EXPRESSIONS = {
    "normal":     expr_custom_normal,
    "happy":      expr_custom_happy,
    "sad":        expr_custom_sad,
    "angry":      expr_custom_angry,
    "surprised":  expr_custom_surprised,
    "sleepy":     expr_custom_sleepy,
    "wink":       expr_custom_wink,
    "love":       expr_custom_love,
    "look_left":  expr_custom_look_left,
    "look_right": expr_custom_look_right,
}


def show_custom_expression(eyes, expr="normal", ew=28, eh=28, rx=10,
                            pupil="medium"):
    """
    Hiển thị biểu cảm với hình dạng mắt tùy chỉnh.

    Tham số:
        eyes   : đối tượng Eyes
        expr   : "normal" | "happy" | "sad" | "angry" | "surprised"
                 "sleepy" | "wink" | "love" | "look_left" | "look_right"
        ew     : chiều rộng mắt, px  [10 – 56]
        eh     : chiều cao mắt, px   [10 – 40]
        rx     : bán kính bo góc, px [0 – min(ew,eh)//2, tự động clamp]
        pupil  : "small" | "medium" | "large"

    Ví dụ:
        show_custom_expression(e, 'happy', ew=36, eh=22, rx=8, pupil='large')
        show_custom_expression(e, 'sad',   ew=16, eh=38, rx=4, pupil='small')
        show_custom_expression(e, 'love',  ew=28, eh=28, rx=14, pupil='large')
    """
    fn = CUSTOM_EXPRESSIONS.get(expr)
    if fn is None:
        raise ValueError("Unknown custom expression: {}".format(expr))
    ew, eh, rx = _validate_custom_params(ew, eh, rx)
    eyes.clear()
    fn(eyes, ew=ew, eh=eh, rx=rx, pupil_size=pupil)
    eyes.show()


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

# eyes.py — Core OLED renderer for Robot Eyes
# ESP32 + MicroPython + SSD1306 128x64
# Usage: from eyes import Eyes

from machine import Pin, SoftI2C
import ssd1306
import framebuf
import time
import math

SCREEN_W = 128
SCREEN_H = 64

# Eye layout constants
EYE_L_CX = 32   # Left eye center X
EYE_R_CX = 96   # Right eye center X
EYE_CY   = 32   # Eye center Y (vertical)
EYE_W    = 28   # Default eye width
EYE_H    = 28   # Default eye height
PUPIL_R  = 6    # Pupil radius


class Eyes:
    def __init__(self, scl_pin=22, sda_pin=21, brightness=255):
        i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.oled = ssd1306.SSD1306_I2C(SCREEN_W, SCREEN_H, i2c)
        self.brightness = brightness
        self.clear()

    # ------------------------------------------------------------------ #
    #  Low-level drawing primitives                                        #
    # ------------------------------------------------------------------ #

    def clear(self):
        self.oled.fill(0)

    def show(self):
        self.oled.show()

    def draw_filled_ellipse(self, cx, cy, rx, ry, color=1):
        """Draw a filled ellipse using horizontal line scan."""
        for dy in range(-ry, ry + 1):
            if ry == 0:
                continue
            frac = 1 - (dy / ry) ** 2
            if frac < 0:
                frac = 0
            dx = int(rx * math.sqrt(frac))
            self.oled.hline(cx - dx, cy + dy, dx * 2 + 1, color)

    def draw_ellipse_outline(self, cx, cy, rx, ry, color=1):
        """Draw ellipse outline using parametric approach."""
        steps = max(rx, ry) * 4
        for i in range(steps):
            angle = 2 * math.pi * i / steps
            x = int(cx + rx * math.cos(angle))
            y = int(cy + ry * math.sin(angle))
            if 0 <= x < SCREEN_W and 0 <= y < SCREEN_H:
                self.oled.pixel(x, y, color)

    def draw_arc(self, cx, cy, r, start_deg, end_deg, color=1, thickness=2):
        """Draw arc from start_deg to end_deg."""
        start_rad = math.radians(start_deg)
        end_rad   = math.radians(end_deg)
        steps = max(20, r * 3)
        for i in range(steps + 1):
            angle = start_rad + (end_rad - start_rad) * i / steps
            for t in range(thickness):
                rr = r - t
                x = int(cx + rr * math.cos(angle))
                y = int(cy + rr * math.sin(angle))
                if 0 <= x < SCREEN_W and 0 <= y < SCREEN_H:
                    self.oled.pixel(x, y, color)

    def clip_rect(self, x, y, w, h, color=0):
        """Fill a rectangle — used to clip/mask part of an eye."""
        self.oled.fill_rect(x, y, w, h, color)

    # ------------------------------------------------------------------ #
    #  Eye drawing                                                         #
    # ------------------------------------------------------------------ #

    def draw_eye(self, cx, cy,
                 ew=EYE_W, eh=EYE_H,
                 pupil_dx=0, pupil_dy=0,
                 top_clip=0, bot_clip=0,
                 closed=False,
                 half_open=False):
        """
        Draw a single eye.
        cx, cy      : center of eye
        ew, eh      : eye width/height (half-axes)
        pupil_dx/dy : pupil offset from center
        top_clip    : pixels to clip from top (angry/sleepy upper lid)
        bot_clip    : pixels to clip from bottom (squint)
        closed      : draw as horizontal line (wink / full blink)
        half_open   : draw only lower half (sleepy)
        """
        rx = ew // 2
        ry = eh // 2

        if closed:
            self.oled.hline(cx - rx, cy, ew, 1)
            self.oled.hline(cx - rx, cy + 1, ew, 1)
            return

        if half_open:
            # Draw only bottom half
            for dy in range(0, ry + 1):
                frac = 1 - (dy / ry) ** 2
                if frac < 0:
                    frac = 0
                dx = int(rx * math.sqrt(frac))
                self.oled.hline(cx - dx, cy + dy, dx * 2 + 1, 1)
            # Top flat line
            self.oled.hline(cx - rx, cy, ew, 1)
            # Pupil in lower half
            self.draw_filled_ellipse(cx + pupil_dx, cy + ry // 2 + pupil_dy, PUPIL_R - 2, PUPIL_R - 1, 0)
            self.oled.pixel(cx + pupil_dx + 2, cy + ry // 2 + pupil_dy - 2, 1)
            return

        # Full eye white
        self.draw_filled_ellipse(cx, cy, rx, ry, 1)

        # Top clip (upper eyelid for angry/sad)
        if top_clip > 0:
            self.clip_rect(cx - rx - 2, cy - ry - 1, ew + 4, top_clip + 1, 0)

        # Bottom clip (lower eyelid squint)
        if bot_clip > 0:
            self.clip_rect(cx - rx - 2, cy + ry - bot_clip, ew + 4, bot_clip + 2, 0)

        # Pupil
        px = cx + pupil_dx
        py = cy + pupil_dy
        self.draw_filled_ellipse(px, py, PUPIL_R, PUPIL_R + 1, 0)

        # Pupil highlight (white dot)
        if 0 <= px + 2 < SCREEN_W and 0 <= py - 2 < SCREEN_H:
            self.oled.pixel(px + 2, py - 2, 1)

    def draw_both_eyes(self, **kwargs):
        """Draw both eyes with same parameters."""
        self.draw_eye(EYE_L_CX, EYE_CY, **kwargs)
        self.draw_eye(EYE_R_CX, EYE_CY, **kwargs)

    def draw_brow(self, cx, angle_deg=0, offset_y=-18, length=20, color=1, thickness=2):
        """
        Draw an eyebrow.
        angle_deg : positive = outer end higher (angry inner), negative = opposite
        """
        rad = math.radians(angle_deg)
        half = length // 2
        x1 = int(cx - half * math.cos(rad))
        y1 = int(EYE_CY + offset_y + half * math.sin(rad))
        x2 = int(cx + half * math.cos(rad))
        y2 = int(EYE_CY + offset_y - half * math.sin(rad))
        for t in range(thickness):
            self.oled.line(x1, y1 + t, x2, y2 + t, color)

    def draw_mouth(self, smile=0, width=20, y_offset=52):
        """
        Draw a mouth arc.
        smile > 0 : happy (arc opens upward)
        smile < 0 : sad   (arc opens downward)
        smile = 0 : flat line
        """
        cx = SCREEN_W // 2
        if smile == 0:
            self.oled.hline(cx - width // 2, y_offset, width, 1)
            self.oled.hline(cx - width // 2, y_offset + 1, width, 1)
            return
        if smile > 0:
            self.draw_arc(cx, y_offset - smile, width // 2, 20, 160, 1, 2)
        else:
            self.draw_arc(cx, y_offset - smile, width // 2, 200, 340, 1, 2)

    # ------------------------------------------------------------------ #
    #  Style A — Rounded Rectangle eye                                    #
    # ------------------------------------------------------------------ #

    def draw_rounded_rect_eye(self, cx, cy,
                               ew=28, eh=28, rx=10,
                               pupil_dx=0, pupil_dy=0,
                               top_clip=0, bot_clip=0,
                               closed=False, half_open=False,
                               top_angle_left=0, top_angle_right=0):
        """
        Draw a single rounded-rectangle eye (Style A).
        cx, cy           : center
        ew, eh           : total width/height of the rect
        rx               : corner radius (4=sharp, 10=balanced, eh//2=pill)
        pupil_dx/dy      : pupil offset
        top_clip         : uniform top clip (sleepy/angry horizontal mask)
        bot_clip         : bottom clip
        closed           : horizontal line (blink/wink)
        half_open        : only lower half visible (sleepy)
        top_angle_left   : extra clip at top-left corner (angry left eye)
        top_angle_right  : extra clip at top-right corner (angry right eye)
        """
        x0 = cx - ew // 2
        y0 = cy - eh // 2

        if closed:
            self.oled.hline(x0, cy, ew, 1)
            self.oled.hline(x0, cy + 1, ew, 1)
            return

        # Draw filled rounded rect using horizontal scan
        for row in range(eh):
            y = y0 + row
            dy = row  # distance from top

            # Compute horizontal extent for this row considering corner radius
            if dy < rx:
                # Top corners — inset based on circle formula
                inset = int(rx - math.sqrt(max(0, rx*rx - (rx - dy)**2)))
            elif dy >= eh - rx:
                # Bottom corners
                ddy = dy - (eh - rx - 1)
                inset = int(rx - math.sqrt(max(0, rx*rx - ddy*ddy)))
            else:
                inset = 0

            x_start = x0 + inset
            x_end   = x0 + ew - inset
            w = x_end - x_start
            if w > 0 and 0 <= y < SCREEN_H:
                self.oled.hline(x_start, y, w, 1)

        # half_open: mask out top half
        if half_open:
            self.oled.fill_rect(x0 - 1, y0 - 1, ew + 2, eh // 2 + 1, 0)
            self.oled.hline(x0, cy, ew, 1)
            # Pupil in lower half
            self.draw_filled_ellipse(cx + pupil_dx, cy + eh // 4 + pupil_dy,
                                     PUPIL_R - 2, PUPIL_R - 1, 0)
            self.oled.pixel(cx + pupil_dx + 2, cy + eh // 4 + pupil_dy - 2, 1)
            return

        # top_clip: horizontal mask from top
        if top_clip > 0:
            self.oled.fill_rect(x0 - 1, y0 - 1, ew + 2, top_clip + 1, 0)

        # bot_clip
        if bot_clip > 0:
            self.oled.fill_rect(x0 - 1, y0 + eh - bot_clip, ew + 2, bot_clip + 2, 0)

        # Angled top-left clip (angry left eye: inner brow pushes down)
        if top_angle_left > 0:
            for col in range(ew):
                clip_h = int(top_angle_left * (ew - col) / ew)
                if clip_h > 0:
                    self.oled.vline(x0 + col, y0, clip_h, 0)

        # Angled top-right clip (angry right eye)
        if top_angle_right > 0:
            for col in range(ew):
                clip_h = int(top_angle_right * col / ew)
                if clip_h > 0:
                    self.oled.vline(x0 + col, y0, clip_h, 0)

        # Pupil
        px = cx + pupil_dx
        py = cy + pupil_dy
        self.draw_filled_ellipse(px, py, PUPIL_R, PUPIL_R + 1, 0)
        if 0 <= px + 2 < SCREEN_W and 0 <= py - 2 < SCREEN_H:
            self.oled.pixel(px + 2, py - 2, 1)

    def draw_both_rounded_rect_eyes(self, **kwargs):
        """Draw both rounded-rect eyes with the same parameters."""
        self.draw_rounded_rect_eye(EYE_L_CX, EYE_CY, **kwargs)
        self.draw_rounded_rect_eye(EYE_R_CX, EYE_CY, **kwargs)

    # ------------------------------------------------------------------ #
    #  Style B — Oggy Oval eye                                            #
    # ------------------------------------------------------------------ #

    def draw_oval_eye(self, cx, cy,
                      outer_rx=26, outer_ry=20,
                      inner_rx=16, inner_ry=14,
                      pupil_dx=0, pupil_dy=0,
                      top_clip=0, bot_clip=0,
                      closed=False, half_open=False,
                      top_angle_left=0, top_angle_right=0):
        """
        Draw a single Oggy-style oval eye (Style B).
        Outer ellipse = dark border/frame.
        Inner ellipse = white eyeball.
        cx, cy             : center
        outer_rx/ry        : outer dark ellipse radii
        inner_rx/ry        : inner white ellipse radii
        pupil_dx/dy        : pupil offset
        top_clip           : pixels masked from top (sleepy/angry)
        bot_clip           : pixels masked from bottom
        closed             : arc line (wink)
        half_open          : sleepy — only lower portion visible
        top_angle_left/right : angled top mask for angry expression
        """
        if closed:
            # Draw a curved arc line instead of filled eye
            self.draw_arc(cx, cy, outer_rx - 2, 190, 350, 1, 3)
            return

        # Draw outer dark ellipse
        self.draw_filled_ellipse(cx, cy, outer_rx, outer_ry, 1)

        # half_open: mask top half of outer ellipse
        if half_open:
            self.oled.fill_rect(cx - outer_rx - 1, cy - outer_ry - 1,
                                 outer_rx * 2 + 2, outer_ry + 1, 0)
            self.oled.hline(cx - outer_rx, cy, outer_rx * 2, 1)
            # Inner white (lower half only)
            for dy in range(0, inner_ry + 1):
                frac = 1 - (dy / inner_ry) ** 2 if inner_ry > 0 else 0
                dx = int(inner_rx * math.sqrt(max(0, frac)))
                self.oled.hline(cx - dx, cy + dy, dx * 2 + 1, 1)
            # Pupil in lower area
            self.draw_filled_ellipse(cx + pupil_dx, cy + inner_ry // 2 + pupil_dy,
                                     PUPIL_R - 1, PUPIL_R, 0)
            self.oled.pixel(cx + pupil_dx + 2, cy + inner_ry // 2 + pupil_dy - 2, 1)
            return

        # Draw inner white ellipse
        self.draw_filled_ellipse(cx, cy, inner_rx, inner_ry, 1)

        # Clips applied AFTER drawing (mask with black)
        if top_clip > 0:
            self.oled.fill_rect(cx - outer_rx - 1, cy - outer_ry - 1,
                                 outer_rx * 2 + 2, top_clip + 1, 0)

        if bot_clip > 0:
            self.oled.fill_rect(cx - outer_rx - 1, cy + outer_ry - bot_clip,
                                 outer_rx * 2 + 2, bot_clip + 2, 0)

        # Angled top-left clip (angry left eye)
        if top_angle_left > 0:
            w = outer_rx * 2
            x0 = cx - outer_rx
            for col in range(w):
                clip_h = int(top_angle_left * (w - col) / w)
                if clip_h > 0:
                    self.oled.vline(x0 + col, cy - outer_ry - 1, clip_h + 1, 0)

        # Angled top-right clip (angry right eye)
        if top_angle_right > 0:
            w = outer_rx * 2
            x0 = cx - outer_rx
            for col in range(w):
                clip_h = int(top_angle_right * col / w)
                if clip_h > 0:
                    self.oled.vline(x0 + col, cy - outer_ry - 1, clip_h + 1, 0)

        # Pupil
        px = cx + pupil_dx
        py = cy + pupil_dy
        self.draw_filled_ellipse(px, py, PUPIL_R, PUPIL_R + 2, 0)
        if 0 <= px + 2 < SCREEN_W and 0 <= py - 2 < SCREEN_H:
            self.oled.pixel(px + 2, py - 2, 1)

    def draw_both_oval_eyes(self, **kwargs):
        """Draw both Oggy oval eyes with the same parameters."""
        self.draw_oval_eye(EYE_L_CX, EYE_CY, **kwargs)
        self.draw_oval_eye(EYE_R_CX, EYE_CY, **kwargs)

    # ------------------------------------------------------------------ #
    #  Render helpers                                                      #
    # ------------------------------------------------------------------ #

    def render(self, draw_fn, *args, **kwargs):
        """Clear, draw, show in one call."""
        self.clear()
        draw_fn(*args, **kwargs)
        self.show()

    def transition(self, from_fn, to_fn, steps=8, delay_ms=30):
        """
        Simple cross-fade transition by alternating frames.
        For OLED, we simulate by blending with checkerboard masks.
        """
        for step in range(steps + 1):
            self.clear()
            if step <= steps // 2:
                from_fn()
            else:
                to_fn()
            self.show()
            time.sleep_ms(delay_ms)

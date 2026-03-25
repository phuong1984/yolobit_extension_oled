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

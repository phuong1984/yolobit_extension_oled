
import time
import gc
from eyes import Eyes, EYE_L_CX, EYE_R_CX, EYE_CY, EYE_W, EYE_H
from expressions import show_expression, EXPRESSIONS, expr_normal

STATE_IDLE = 0
STATE_RUNNING = 1
STATE_PAUSED = 2
STATE_DONE = 3

_BLINK_CLOSE = (0.3, 0.6, 0.85, 1.0)
_BLINK_OPEN = (0.7, 0.4, 0.15, 0.0)
_LOOK_AROUND_SEQUENCE = [(-6, 0), (0, 0), (6, 0), (0, 0), (0, -4), (0, 4), (0, 0)]
_DIZZY_FRAMES = [
    (int(5 * __import__('math').cos(2 * __import__('math').pi * i / 12)),
     int(4 * __import__('math').sin(2 * __import__('math').pi * i / 12)))
    for i in range(12)
]
_WAKE_UP_STAGES = [(1, True, False), (1, True, False), (0, True, False), (0, False, False)]


class Animation:
    """Base class cho non-blocking animations."""
    
    def __init__(self, eyes: Eyes):
        self.eyes = eyes
        self.state = STATE_IDLE
        self.frame = 0
        self.last_update = 0
        self.delay = 16 
    
    def init(self):
        self.state = STATE_RUNNING
        self.frame = 0
        self.last_update = time.ticks_ms()
    
    def update(self):
        """
        Trả về True nếu animation ĐANG CHẠY.
        Trả về False nếu animation ĐÃ XONG.
        """
        if self.state == STATE_DONE:
            return False # Không tự động init lại ở đây, Manager sẽ quyết định
        
        if self.state == STATE_PAUSED:
            return True

        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_update) < self.delay:
            return True 

        self.last_update = now
        self._run_frame()

        if self._is_finished():
            self.state = STATE_DONE
            self._cleanup()
            return False # Báo hiệu đã xong
        
        return True
    
    def _run_frame(self):
        pass
    
    def _is_finished(self):
        return False
    
    def _cleanup(self):
        gc.collect()
    
    def reset(self):
        self.state = STATE_IDLE
        self.frame = 0


class BlinkAnimation(Animation):
    def init(self):
        super().init()
        self.delay = 30
        self.phase = "close"
        self.step = 0
        self.hold_start = 0

    def _run_frame(self):
        if self.phase == "close":
            if self.step < len(_BLINK_CLOSE):
                clip = int(EYE_H * _BLINK_CLOSE[self.step])
                self.eyes.clear()
                _draw_closing_eyes(self.eyes, clip)
                self.eyes.show()
                self.step += 1
            else:
                self.phase = "hold"
                self.hold_start = time.ticks_ms()

        elif self.phase == "hold":
            if time.ticks_diff(time.ticks_ms(), self.hold_start) >= 60:
                self.phase = "open"
                self.step = 0

        elif self.phase == "open":
            if self.step < len(_BLINK_OPEN):
                clip = int(EYE_H * _BLINK_OPEN[self.step])
                self.eyes.clear()
                _draw_closing_eyes(self.eyes, clip)
                self.eyes.show()
                self.step += 1
            else:
                self.frame = 999 

    def _is_finished(self):
        return self.frame >= 999


def _draw_closing_eyes(e: Eyes, clip_amount: int):
    for cx in (EYE_L_CX, EYE_R_CX):
        e.draw_eye(cx, EYE_CY, bot_clip=clip_amount, top_clip=max(0, clip_amount - EYE_H // 2))
    e.draw_mouth(smile=0, width=18)


class LookAroundAnimation(Animation):
    def init(self):
        super().init()
        self.delay = 200
        self.step = 0
    
    def _run_frame(self):
        if self.step < len(_LOOK_AROUND_SEQUENCE):
            dx, dy = _LOOK_AROUND_SEQUENCE[self.step]
            self.eyes.clear()
            self.eyes.draw_both_eyes(pupil_dx=dx, pupil_dy=dy)
            self.eyes.draw_mouth(smile=0, width=18)
            self.eyes.show()
            self.step += 1
        else:
            self.frame = 999
    
    def _is_finished(self):
        return self.frame >= 999


class DizzyAnimation(Animation):
    def init(self):
        super().init()
        self.delay = 60
        self.step = 0
    
    def _run_frame(self):
        if self.step < len(_DIZZY_FRAMES):
            dx, dy = _DIZZY_FRAMES[self.step]
            self.eyes.clear()
            self.eyes.draw_both_eyes(pupil_dx=dx, pupil_dy=dy)
            self.eyes.oled.hline(54, 20, 4, 1)
            self.eyes.oled.hline(70, 16, 4, 1)
            self.eyes.show()
            self.step += 1
        else:
            self.frame = 999
    
    def _is_finished(self):
        return self.frame >= 999


class WakeUpAnimation(Animation):
    def init(self):
        super().init()
        self.delay = 80
        self.step = 0
        self.blink_done = False
        self.blink_anim = None
    
    def _run_frame(self):
        if not self.blink_done:
            if self.step < len(_WAKE_UP_STAGES):
                top, half, _ = _WAKE_UP_STAGES[self.step]
                self.eyes.clear()
                self.eyes.draw_eye(EYE_L_CX, EYE_CY, half_open=half)
                self.eyes.draw_eye(EYE_R_CX, EYE_CY, half_open=half)
                self.eyes.show()
                self.step += 1
            else:
                self.blink_anim = BlinkAnimation(self.eyes)
                self.blink_anim.init()
                self.blink_done = True
        else:
            if self.blink_anim:
                # CHỈ gọi update() một lần duy nhất mỗi frame
                is_running = self.blink_anim.update()
                if not is_running:
                    show_expression(self.eyes, "normal")
                    self.frame = 999
    
    def _is_finished(self):
        return self.frame >= 999

class ShockedAnimation(Animation):
    def init(self):
        super().init()
        self.delay = 100
        self.phase = "wait"
        self.shake_count = 0
        self.shake_dir = 1
        self.blink_anim = None
    
    def _run_frame(self):
        if self.phase == "wait":
            show_expression(self.eyes, "normal")
            self.phase = "blink"
            self.blink_anim = BlinkAnimation(self.eyes)
            self.blink_anim.init()

        elif self.phase == "blink":
            if self.blink_anim:
                # CHỈ gọi update() một lần duy nhất mỗi frame
                is_running = self.blink_anim.update()
                if not is_running:
                    show_expression(self.eyes, "surprised")
                    self.phase = "shake"
                    self.shake_count = 0
                    self.shake_dir = 1
                    self.delay = 30 # Tăng tốc độ rung

        elif self.phase == "shake":
            if self.shake_count < 4:
                offset = self.shake_dir * 2
                self.eyes.oled.scroll(offset, 0)
                self.eyes.show()
                self.shake_count += 1
                self.shake_dir = -self.shake_dir
            else:
                self.frame = 999

    def _is_finished(self):
        return self.frame >= 999
    
class HappyBounceAnimation(Animation):
    def init(self):
        super().init()
        self.delay = 100
        self.step = 0
        self.show_phase = True
    
    def _run_frame(self):
        if self.show_phase:
            show_expression(self.eyes, "happy")
            self.show_phase = False
        else:
            self.eyes.clear()
            self.eyes.draw_both_eyes(pupil_dy=-3)
            self.eyes.draw_mouth(smile=10, width=28)
            self.eyes.show()
            self.show_phase = True
            self.step += 1
            
            if self.step >= 6:
                show_expression(self.eyes, "happy")
                self.frame = 999

    def _is_finished(self):
        return self.frame >= 999

ANIMATION_CLASSES = {
    "blink": BlinkAnimation,
    "look_around": LookAroundAnimation,
    "dizzy": DizzyAnimation,
    "wake_up": WakeUpAnimation,
    "shocked": ShockedAnimation,
    "happy_bounce": HappyBounceAnimation,
}


def create_animation(eyes: Eyes, name: str):
    cls = ANIMATION_CLASSES.get(name)
    if cls is None:
        raise ValueError("Unknown animation: {}".format(name))
    return cls(eyes)


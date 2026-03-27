// English language file for Robot Eyes OLED extension
// This file contains all messages and tooltips for the Blockly blocks

// ==================================================================
// ROBOT SETUP BLOCK
// ==================================================================
Blockly.Msg.ROBOT_EYES_SETUP_MESSAGE = "🤖 Robot Eyes Init"
Blockly.Msg.ROBOT_EYES_SETUP_TOOLTIP = "Initialize the OLED display"
Blockly.Msg.ROBOT_EYES_SETUP_HELPURL = ""

// ==================================================================
// PLAY ANIMATION BLOCK (BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_PLAY_ANIMATION_MESSAGE = "✨ Play %1 Times: %2 Speed: %3"
Blockly.Msg.ROBOT_PLAY_ANIMATION_TOOLTIP = "BLOCKING: Plays animation and WAITS until complete before continuing. Use for simple sequences. Do NOT use inside 'while True' loops. CPU is blocked during animation."
Blockly.Msg.ROBOT_PLAY_ANIMATION_HELPURL = ""

// Animation dropdown options
Blockly.Msg.ANIMATION_BLINK = "👁 Blink"
Blockly.Msg.ANIMATION_LOOK_AROUND = "👀 Look Around"
Blockly.Msg.ANIMATION_DIZZY = "💫 Dizzy"
Blockly.Msg.ANIMATION_WAKE_UP = "😴→😊 Wake Up"
Blockly.Msg.ANIMATION_SHOCKED = "😱 Shocked"
Blockly.Msg.ANIMATION_HAPPY_BOUNCE = "😊 Happy Bounce"
Blockly.Msg.ANIMATION_IDLE = "🔁 Idle Blink"

// Speed dropdown options
Blockly.Msg.SPEED_NORMAL = "Normal (1×)"
Blockly.Msg.SPEED_FAST = "Fast (2×)"
Blockly.Msg.SPEED_SLOW = "Slow (0.5×)"

// ==================================================================
// CREATE ANIMATION BLOCK (NON-BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_MESSAGE = "✨ Create Animation (non-blocking) %1"
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_TOOLTIP = "NON-BLOCKING: Use inside 'while True' loop. Creates animation object. Call update block each frame. Animation speed depends on time.sleep_ms() in your loop (e.g., 16ms=fast, 100ms=slow)."
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_HELPURL = ""

// ==================================================================
// UPDATE ANIMATION BLOCK (NON-BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_MESSAGE = "🔄 Update Animation (non-blocking)"
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_TOOLTIP = "Updates non-blocking animation by one frame. Use inside 'while True' loop after creating animation. Returns True if animation still running."
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_HELPURL = ""

// ==================================================================
// SHOW SQUARE EXPRESSION BLOCK
// ==================================================================
Blockly.Msg.ROBOT_SHOW_SQUARE_MESSAGE = "⬜ Square Eyes  Shape: %1  Face: %2"
Blockly.Msg.ROBOT_SHOW_SQUARE_TOOLTIP = "Style A: Rounded rectangle eyes. Choose a shape and an expression."
Blockly.Msg.ROBOT_SHOW_SQUARE_HELPURL = ""

// Square shape dropdown options
Blockly.Msg.SQUARE_SHAPE_SHARP = "⬜ Sharp (rx=4)"
Blockly.Msg.SQUARE_SHAPE_BALANCED = "🔲 Balanced (rx=10)"
Blockly.Msg.SQUARE_SHAPE_ROUND = "🔘 Round (rx=14)"
Blockly.Msg.SQUARE_SHAPE_WIDE = "▬ Wide flat"

// ==================================================================
// SHOW OVAL EXPRESSION BLOCK
// ==================================================================
Blockly.Msg.ROBOT_SHOW_OVAL_MESSAGE = "👁 Oval Eyes  Shape: %1  Face: %2"
Blockly.Msg.ROBOT_SHOW_OVAL_TOOLTIP = "Style B: Oggy-style oval eyes. Choose a shape and an expression."
Blockly.Msg.ROBOT_SHOW_OVAL_HELPURL = ""

// Oval shape dropdown options
Blockly.Msg.OVAL_SHAPE_NORMAL = "🔵 Normal oval"
Blockly.Msg.OVAL_SHAPE_WIDE = "🏈 Wide flat"
Blockly.Msg.OVAL_SHAPE_TALL = "🥚 Tall oval"
Blockly.Msg.OVAL_SHAPE_BIG = "👁 Big bubble"

// ==================================================================
// EXPRESSION DROPDOWN OPTIONS (shared for square and oval)
// ==================================================================
Blockly.Msg.EXPR_NORMAL = "😐 Normal"
Blockly.Msg.EXPR_HAPPY = "😊 Happy"
Blockly.Msg.EXPR_SAD = "😢 Sad"
Blockly.Msg.EXPR_ANGRY = "😠 Angry"
Blockly.Msg.EXPR_SURPRISED = "😲 Surprised"
Blockly.Msg.EXPR_SLEEPY = "😴 Sleepy"
Blockly.Msg.EXPR_WINK = "😉 Wink"
Blockly.Msg.EXPR_LOVE = "😍 Love"
Blockly.Msg.EXPR_LOOK_LEFT = "👀 Look Left"
Blockly.Msg.EXPR_LOOK_RIGHT = "👀 Look Right"

// ==================================================================
// Custom expression block
// ==================================================================
Blockly.Msg.ROBOT_SHOW_CUSTOM_MESSAGE =
    "Custom eyes  Face: %1  Eye width: %2 px  Eye height: %3 px  Corner radius: %4 px  Pupil: %5";

// --- Dropdown: pupil size ---
Blockly.Msg.PUPIL_SMALL  = "small";
Blockly.Msg.PUPIL_MEDIUM = "medium";
Blockly.Msg.PUPIL_LARGE  = "large";

// --- Tooltip & helpURL ---
Blockly.Msg.ROBOT_SHOW_CUSTOM_TOOLTIP =
    "Display a facial expression with custom eye shape. " +
    "Width: 10–56 px, Height: 10–40 px, " +
    "Corner radius: 0 (sharp) to min(w,h)/2 (pill shape). " +
    "The corner radius is automatically clamped if too large. " +
    "Pupil size scales with the eye width.";
Blockly.Msg.ROBOT_SHOW_CUSTOM_HELPURL = "";

// ==================================================================
// ANIMATE CUSTOM EYES (NON-BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_ANIMATE_CUSTOM_MESSAGE = "🎬 Animate custom eyes %1";

Blockly.Msg.ANIMATE_MODE_IDLE = "idle (stay in place)";
Blockly.Msg.ANIMATE_MODE_MOVE = "move (travel around)";
Blockly.Msg.ANIMATE_MODE_ACTION = "action (special behavior)";
Blockly.Msg.ANIMATE_MODE_ALL = "all (cycle: idle → move → action)";

Blockly.Msg.ROBOT_ANIMATE_CUSTOM_TOOLTIP =
    "NON-BLOCKING: Animate custom eyes with behavior based on expression. " +
    "idle: Stay in place with expression-specific idle animation. " +
    "move: Travel around screen with expression-specific movement. " +
    "action: Perform expression-specific special action. " +
    "all: Cycle through idle (2s) → move (3s) → action → repeat. " +
    "Create custom eyes before using this block. " +
    "Use in 'while True' loop. Call repeatedly each frame.";
Blockly.Msg.ROBOT_ANIMATE_CUSTOM_HELPURL = "";

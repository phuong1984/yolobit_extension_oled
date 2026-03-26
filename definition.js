/**
 * definition.js — Blockly custom block definitions for Robot Eyes
 * ESP32 + MicroPython + SSD1306 128x64
 *
 * Style: jsonInit (OhStem standard)
 * Usage: load AFTER blockly.min.js in your HTML
 * 
 * Note: All messages and tooltips are loaded from languages/en.js and languages/vi.js
 */

'use strict';

/* ================================================================== *
 *  COLOUR                                                             *
 * ================================================================== */
const ROBOT_EYES_COLOR = '#E85D24';

/* ================================================================== *
 *  DROPDOWN OPTIONS - ANIMATION                                       *
 * ================================================================== */
const ANIMATION_OPTIONS = [
  [Blockly.Msg.ANIMATION_BLINK,        'blink'],
  [Blockly.Msg.ANIMATION_LOOK_AROUND,  'look_around'],
  [Blockly.Msg.ANIMATION_DIZZY,        'dizzy'],
  [Blockly.Msg.ANIMATION_WAKE_UP,      'wake_up'],
  [Blockly.Msg.ANIMATION_SHOCKED,      'shocked'],
  [Blockly.Msg.ANIMATION_HAPPY_BOUNCE, 'happy_bounce'],
  [Blockly.Msg.ANIMATION_IDLE,         'idle'],
];

/* ================================================================== *
 *  DROPDOWN OPTIONS - SPEED                                           *
 * ================================================================== */
const SPEED_OPTIONS = [
  [Blockly.Msg.SPEED_NORMAL, '1.0'],
  [Blockly.Msg.SPEED_FAST,   '2.0'],
  [Blockly.Msg.SPEED_SLOW,   '0.5'],
];

/* ================================================================== *
 *  DROPDOWN OPTIONS - EXPRESSION (for square and oval eyes)           *
 * ================================================================== */
const EXPR_OPTIONS = [
  [Blockly.Msg.EXPR_NORMAL,     'normal'],
  [Blockly.Msg.EXPR_HAPPY,      'happy'],
  [Blockly.Msg.EXPR_SAD,        'sad'],
  [Blockly.Msg.EXPR_ANGRY,      'angry'],
  [Blockly.Msg.EXPR_SURPRISED,  'surprised'],
  [Blockly.Msg.EXPR_SLEEPY,     'sleepy'],
  [Blockly.Msg.EXPR_WINK,       'wink'],
  [Blockly.Msg.EXPR_LOVE,       'love'],
  [Blockly.Msg.EXPR_LOOK_LEFT,  'look_left'],
  [Blockly.Msg.EXPR_LOOK_RIGHT, 'look_right'],
];

/* ================================================================== *
 *  DROPDOWN OPTIONS - SQUARE SHAPE                                    *
 * ================================================================== */
const SQUARE_SHAPE_OPTIONS = [
  [Blockly.Msg.SQUARE_SHAPE_SHARP,     'sharp'],
  [Blockly.Msg.SQUARE_SHAPE_BALANCED,  'balanced'],
  [Blockly.Msg.SQUARE_SHAPE_ROUND,     'round'],
  [Blockly.Msg.SQUARE_SHAPE_WIDE,      'wide'],
];

/* ================================================================== *
 *  DROPDOWN OPTIONS - OVAL SHAPE                                      *
 * ================================================================== */
const OVAL_SHAPE_OPTIONS = [
  [Blockly.Msg.OVAL_SHAPE_NORMAL,  'normal'],
  [Blockly.Msg.OVAL_SHAPE_WIDE,    'wide'],
  [Blockly.Msg.OVAL_SHAPE_TALL,    'tall'],
  [Blockly.Msg.OVAL_SHAPE_BIG,     'big'],
];

/* ================================================================== *
 *  1. ROBOT EYES SETUP                                                *
 * ================================================================== */
Blockly.Blocks['robot_setup'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_setup",
      "message0": Blockly.Msg.ROBOT_EYES_SETUP_MESSAGE,
      "previousStatement": null,
      "nextStatement": null,
      "colour": ROBOT_EYES_COLOR,
      "tooltip": Blockly.Msg.ROBOT_EYES_SETUP_TOOLTIP,
      "helpUrl": Blockly.Msg.ROBOT_EYES_SETUP_HELPURL
    });
  }
};

Blockly.Python['robot_setup'] = function(block) {
  Blockly.Python.definitions_['import_yolobit'] = 'from yolobit import *';
  Blockly.Python.definitions_['import_i2c'] = 'from machine import Pin';
  Blockly.Python.definitions_['import_eyes'] = 'from eyes import Eyes';
  Blockly.Python.definitions_['import_expressions'] = 'from expressions import show_expression';
  Blockly.Python.definitions_['import_animations'] = 'from animations import play_animation';
  Blockly.Python.definitions_['import_show_custom'] = 'from expressions import show_custom_expression';
  Blockly.Python.definitions_['import_time'] = 'import time';

  var code = 'e = Eyes(scl_pin=Pin(pin19.pin), sda_pin=Pin(pin20.pin))\n';
  return code;
};

/* ================================================================== *
 *  2. PLAY ANIMATION (BLOCKING)                                       *
 * ================================================================== */
Blockly.Blocks['robot_play_animation'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_play_animation",
      "message0": Blockly.Msg.ROBOT_PLAY_ANIMATION_MESSAGE,
      "args0": [
        {
          "type": "field_dropdown",
          "name": "ANIM",
          "options": ANIMATION_OPTIONS
        },
        {
          "type": "field_number",
          "name": "TIMES",
          "value": 1,
          "min": 1,
          "max": 20
        },
        {
          "type": "field_dropdown",
          "name": "SPEED",
          "options": SPEED_OPTIONS
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": ROBOT_EYES_COLOR,
      "tooltip": Blockly.Msg.ROBOT_PLAY_ANIMATION_TOOLTIP,
      "helpUrl": Blockly.Msg.ROBOT_PLAY_ANIMATION_HELPURL
    });
  }
};

Blockly.Python['robot_play_animation'] = function(block) {
  var dropdown_anim = block.getFieldValue('ANIM');
  var number_times = block.getFieldValue('TIMES');
  var dropdown_speed = block.getFieldValue('SPEED');
  var code = 'play_animation(e, \'' + dropdown_anim + '\', times=' + number_times + ', speed=' + dropdown_speed + ')\n';
  return code;
};

/* ================================================================== *
 *  3. CREATE ANIMATION (NON-BLOCKING)                                 *
 * ================================================================== */
Blockly.Blocks['robot_create_animation_nb'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_create_animation_nb",
      "message0": Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_MESSAGE,
      "args0": [
        {
          "type": "field_dropdown",
          "name": "ANIM",
          "options": ANIMATION_OPTIONS
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": ROBOT_EYES_COLOR,
      "tooltip": Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_TOOLTIP,
      "helpUrl": Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_HELPURL
    });
  }
};

Blockly.Python['robot_create_animation_nb'] = function(block) {
  Blockly.Python.definitions_['import_nonblocking'] = 'from nonblocking_anim import create_animation';
  var dropdown_anim = block.getFieldValue('ANIM');
  var code = '# Non-blocking animation - creates animation object\n';
  code += '# Initialize variable if not exists\n';
  code += 'try:\n';
  code += '    current_anim\n';
  code += 'except NameError:\n';
  code += '    current_anim = None\n';
  code += '\n';
  code += '# Speed depends on time.sleep_ms() in your loop (16ms=fast, 100ms=slow)\n';
  code += 'if current_anim is None:\n';
  code += '    current_anim = create_animation(e, \'' + dropdown_anim + '\')\n';
  code += '    current_anim.init()\n';
  return code;
};

/* ================================================================== *
 *  4. UPDATE ANIMATION (NON-BLOCKING)                                 *
 * ================================================================== */
Blockly.Blocks['robot_update_animation_nb'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_update_animation_nb",
      "message0": Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_MESSAGE,
      "previousStatement": null,
      "nextStatement": null,
      "colour": ROBOT_EYES_COLOR,
      "tooltip": Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_TOOLTIP,
      "helpUrl": Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_HELPURL
    });
  }
};

Blockly.Python['robot_update_animation_nb'] = function(block) {
  var code = '# Update animation frame\n';
  code += '# Initialize variable if not exists\n';
  code += 'try:\n';
  code += '    current_anim\n';
  code += 'except NameError:\n';
  code += '    current_anim = None\n';
  code += '\n';
  code += '# Update animation (auto-restarts when done)\n';
  code += 'if current_anim is not None:\n';
  code += '    current_anim.update()  # Returns True always (auto-restart)\n';
  return code;
};

/* ================================================================== *
 *  5. SHOW SQUARE EXPRESSION                                          *
 * ================================================================== */
Blockly.Blocks['robot_show_square'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_show_square",
      "message0": Blockly.Msg.ROBOT_SHOW_SQUARE_MESSAGE,
      "args0": [
        {
          "type": "field_dropdown",
          "name": "SHAPE",
          "options": SQUARE_SHAPE_OPTIONS
        },
        {
          "type": "field_dropdown",
          "name": "EXPR",
          "options": EXPR_OPTIONS
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "#533AB7",
      "tooltip": Blockly.Msg.ROBOT_SHOW_SQUARE_TOOLTIP,
      "helpUrl": Blockly.Msg.ROBOT_SHOW_SQUARE_HELPURL
    });
  }
};

Blockly.Python['robot_show_square'] = function(block) {
  Blockly.Python.definitions_['import_show_square'] = 'from expressions import show_square_expression';
  var shape = block.getFieldValue('SHAPE');
  var expr = block.getFieldValue('EXPR');
  return 'show_square_expression(e, shape=\'' + shape + '\', expr=\'' + expr + '\')\n';
};

/* ================================================================== *
 *  6. SHOW OVAL EXPRESSION                                            *
 * ================================================================== */
Blockly.Blocks['robot_show_oval'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_show_oval",
      "message0": Blockly.Msg.ROBOT_SHOW_OVAL_MESSAGE,
      "args0": [
        {
          "type": "field_dropdown",
          "name": "SHAPE",
          "options": OVAL_SHAPE_OPTIONS
        },
        {
          "type": "field_dropdown",
          "name": "EXPR",
          "options": EXPR_OPTIONS
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "#0F6E56",
      "tooltip": Blockly.Msg.ROBOT_SHOW_OVAL_TOOLTIP,
      "helpUrl": Blockly.Msg.ROBOT_SHOW_OVAL_HELPURL
    });
  }
};

Blockly.Python['robot_show_oval'] = function(block) {
  Blockly.Python.definitions_['import_show_oval'] = 'from expressions import show_oval_expression';
  var shape = block.getFieldValue('SHAPE');
  var expr = block.getFieldValue('EXPR');
  return 'show_oval_expression(e, shape=\'' + shape + '\', expr=\'' + expr + '\')\n';
};


/* ================================================================== *
 *  DROPDOWN OPTIONS — PUPIL SIZE                                      *
 * ================================================================== */
const PUPIL_SIZE_OPTIONS = [
  [Blockly.Msg.PUPIL_SMALL,  'small'],
  [Blockly.Msg.PUPIL_MEDIUM, 'medium'],
  [Blockly.Msg.PUPIL_LARGE,  'large'],
];

/* ================================================================== *
 *  7. SHOW CUSTOM EXPRESSION                                          *
 * ================================================================== */
Blockly.Blocks['robot_show_custom'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_show_custom",
      "message0": Blockly.Msg.ROBOT_SHOW_CUSTOM_MESSAGE,
      // Blockly.Msg.ROBOT_SHOW_CUSTOM_MESSAGE nên là chuỗi như:
      // "Hiển thị biểu cảm %1 mắt rộng %2 px cao %3 px bo góc %4 px con ngươi %5"
      "args0": [
        {
          "type": "field_dropdown",
          "name": "EXPR",
          "options": EXPR_OPTIONS   // tái dùng từ block square/oval
        },
        {
          "type": "field_number",
          "name": "EW",
          "value": 28,
          "min": 10,
          "max": 56,
          "precision": 1
        },
        {
          "type": "field_number",
          "name": "EH",
          "value": 28,
          "min": 10,
          "max": 40,
          "precision": 1
        },
        {
          "type": "field_number",
          "name": "RX",
          "value": 6,
          "min": 0,
          "max": 20,   // Blockly cap — Python sẽ clamp thêm về min(ew,eh)//2
          "precision": 1
        },
        {
          "type": "field_dropdown",
          "name": "PUPIL",
          "options": PUPIL_SIZE_OPTIONS
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": "#7C4EBF",   // màu tím nhạt — phân biệt với square (#533AB7) và oval (#0F6E56)
      "tooltip": Blockly.Msg.ROBOT_SHOW_CUSTOM_TOOLTIP,
      "helpUrl": Blockly.Msg.ROBOT_SHOW_CUSTOM_HELPURL
    });
  }
};

Blockly.Python['robot_show_custom'] = function(block) {
  Blockly.Python.definitions_['import_show_custom'] = 'from expressions import show_custom_expression';

  var expr   = block.getFieldValue('EXPR');
  var ew     = block.getFieldValue('EW');
  var eh     = block.getFieldValue('EH');
  var rx     = block.getFieldValue('RX');
  var pupil  = block.getFieldValue('PUPIL');

  // Blockly number fields trả về string — ép kiểu int để an toàn
  var code =
      'show_custom_expression(e, ' +
      'expr=\'' + expr   + '\', ' +
      'ew='     + parseInt(ew)    + ', ' +
      'eh='     + parseInt(eh)    + ', ' +
      'rx='     + parseInt(rx)    + ', ' +
      'pupil=\''+ pupil  + '\')\n';
  return code;
};

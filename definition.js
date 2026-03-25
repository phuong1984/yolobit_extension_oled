/**
 * definition.js — Blockly custom block definitions for Robot Eyes
 * ESP32 + MicroPython + SSD1306 128x64
 *
 * Style: jsonInit (OhStem standard)
 * Usage: load AFTER blockly.min.js in your HTML
 */

'use strict';

console.log('[Robot Eyes] Loading definition.js...');

/* ================================================================== *
 *  COLOUR                                                             *
 * ================================================================== */
const ROBOT_EYES_COLOR = '#E85D24';

/* ================================================================== *
 *  DROPDOWN OPTIONS                                                   *
 * ================================================================== */
const EXPRESSION_OPTIONS = [
  ['😐 Normal',    'normal'],
  ['😊 Happy',     'happy'],
  ['😢 Sad',       'sad'],
  ['😠 Angry',     'angry'],
  ['😲 Surprised', 'surprised'],
  ['😴 Sleepy',    'sleepy'],
  ['😕 Confused',  'confused'],
  ['😍 Love',      'love'],
  ['😉 Wink',      'wink'],
  ['👀 Look Left', 'look_left'],
  ['👀 Look Right','look_right'],
];

const ANIMATION_OPTIONS = [
  ['👁 Blink',        'blink'],
  ['👀 Look Around',  'look_around'],
  ['💫 Dizzy',        'dizzy'],
  ['😴→😊 Wake Up',   'wake_up'],
  ['😱 Shocked',      'shocked'],
  ['😊 Happy Bounce', 'happy_bounce'],
  ['🔁 Idle Blink',   'idle'],
];

const SPEED_OPTIONS = [
  ['Normal (1×)', '1.0'],
  ['Fast (2×)',   '2.0'],
  ['Slow (0.5×)', '0.5'],
];

/* ================================================================== *
 *  1. ROBOT EYES SETUP (simple statement block)                       *
 * ================================================================== */
Blockly.Blocks['robot_setup'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_setup",
      "message0": "🤖 Robot Eyes Setup",
      "previousStatement": null,
      "nextStatement": null,
      "colour": ROBOT_EYES_COLOR,
      "tooltip": "Initialize the OLED display",
      "helpUrl": ""
    });
  }
};

Blockly.Python['robot_setup'] = function(block) {
  Blockly.Python.definitions_['import_yolobit'] = 'from yolobit import *';
  Blockly.Python.definitions_['import_i2c'] = 'from machine import Pin';
  Blockly.Python.definitions_['import_eyes'] = 'from eyes import Eyes';
  Blockly.Python.definitions_['import_expressions'] = 'from expressions import show_expression';
  Blockly.Python.definitions_['import_animations'] = 'from animations import play_animation';
  Blockly.Python.definitions_['import_time'] = 'import time';
  
  var code = 'e = Eyes(scl_pin=Pin(pin19.pin), sda_pin=Pin(pin20.pin))\n';
  return code;
};

/* ================================================================== *
 *  2. SHOW EXPRESSION                                                 *
 * ================================================================== */
Blockly.Blocks['robot_show_expression'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_show_expression",
      "message0": "😊 Show %1",
      "args0": [
        {
          "type": "field_dropdown",
          "name": "EXPR",
          "options": EXPRESSION_OPTIONS
        }
      ],
      "previousStatement": null,
      "nextStatement": null,
      "colour": ROBOT_EYES_COLOR,
      "tooltip": "Display a facial expression on the OLED screen.",
      "helpUrl": ""
    });
  }
};

Blockly.Python['robot_show_expression'] = function(block) {
  var dropdown_expr = block.getFieldValue('EXPR');
  var code = 'show_expression(e, \'' + dropdown_expr + '\')\n';
  return code;
};

/* ================================================================== *
 *  3. PLAY ANIMATION                                                  *
 * ================================================================== */
Blockly.Blocks['robot_play_animation'] = {
  init: function() {
    this.jsonInit({
      "type": "robot_play_animation",
      "message0": "✨ Play %1 × %2 Speed: %3",
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
      "tooltip": "Play a built-in animation sequence.",
      "helpUrl": ""
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

Blockly.Blocks['oled_create'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "oled_create",
        "message0": Blockly.Msg.BLOCK_OLED_CREATE_MESSAGE0,
        "args0": [
          {
            "type": "field_variable",
            "name": "oled_lcd",
            "variable": Blockly.Msg.BLOCK_OLED_CREATE_MESSAGE1,
          },
          {
            "type": "field_number",
            "name": "WIDTH",
            "value": 128,
            "min": 0
          },
          {
            "type": "field_number",
            "name": "HEIGHT",
            "value": 64,
            "min": 0
          },
          {
            "type": "field_input",
            "name": "ADDR",
            "text": "0x3c"
          }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#27b0ba",
        "tooltip": Blockly.Msg.BLOCK_OLED_CREATE_TOOLTIP,
        "helpUrl": Blockly.Msg.BLOCK_OLED_CREATE_HELPURL
      }
    );
  }
};

Blockly.Python['oled_create'] = function(block) {
  var variable_oled_lcd = Blockly.Python.variableDB_.getName(block.getFieldValue('oled_lcd'), Blockly.Variables.NAME_TYPE);
  var number_width = block.getFieldValue('WIDTH');
  var number_height = block.getFieldValue('HEIGHT');
  var text_addr = block.getFieldValue('ADDR');
  // TODO: Assemble Python into code variable.
  Blockly.Python.definitions_['import_yolobit'] = 'from yolobit import *';
  Blockly.Python.definitions_['import_i2c'] = 'from machine import Pin, SoftI2C';
  Blockly.Python.definitions_['import_oled'] = 'from ssd1306 import SSD1306_I2C';
  // oled = SSD1306_I2C(oled_width, oled_height, i2c)
  var code = variable_oled_lcd + ' = SSD1306_I2C(' + number_width + ', ' + number_height + ', SoftI2C(scl=Pin(pin19.pin), sda=Pin(pin20.pin)))\n';
  return code;
};

Blockly.Blocks['oled_text'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "oled_text",
        "message0": Blockly.Msg.BLOCK_OLED_TEXT_MESSAGE0,
        "args0": [
          {
            "type": "field_variable",
            "name": "oled_lcd",
            "variable": Blockly.Msg.BLOCK_OLED_TEXT_MESSAGE1,
          },
          {
            "type": "input_dummy"
          },
          {
            "type": "input_value",
            "name": "TEXT"
          },
          {
            "type": "input_value",
            "name": "X",
            "check": "Number"
          },
          {
            "type": "input_value",
            "name": "Y",
            "check": "Number"
          },
          {
            "type": "field_dropdown",
            "name": "COLOR",
            "options": [
              [
                Blockly.Msg.BLOCK_OLED_TEXT_MESSAGE2, //white
                "1"
              ],
              [
                Blockly.Msg.BLOCK_OLED_TEXT_MESSAGE3, //black
                "0"
              ]
            ]
          }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#27b0ba",
        "tooltip": Blockly.Msg.BLOCK_OLED_TEXT_TOOLTIP,
        "helpUrl": Blockly.Msg.BLOCK_OLED_TEXT_HELPURL
      }
    );
  }
};

Blockly.Python['oled_text'] = function(block) {
  var variable_oled_lcd = Blockly.Python.variableDB_.getName(block.getFieldValue('oled_lcd'), Blockly.Variables.NAME_TYPE);
  var value_text = Blockly.Python.valueToCode(block, 'TEXT', Blockly.Python.ORDER_ATOMIC);
  var value_x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC);
  var value_y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC);
  var dropdown_color = block.getFieldValue('COLOR');
  // TODO: Assemble Python into code variable.
  //oled.text('Hello, World 1!', 0, 0, col); oled.show()
  var code = variable_oled_lcd + '.text(str(' + value_text + '), ' + value_x + ', ' + value_y + ', ' + dropdown_color + '); ' + variable_oled_lcd + '.show()\n';
  return code;
};

Blockly.Blocks['oled_fill'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "oled_fill",
        "message0": Blockly.Msg.BLOCK_OLED_FILL_MESSAGE0,
        "args0": [
          {
            "type": "field_variable",
            "name": "oled_lcd",
            "variable": Blockly.Msg.BLOCK_OLED_FILL_MESSAGE1,
          },
          {
            "type": "field_dropdown",
            "name": "COLOR",
            "options": [
              [
                Blockly.Msg.BLOCK_OLED_FILL_MESSAGE2, //black
                "0"
              ],
              [
                Blockly.Msg.BLOCK_OLED_FILL_MESSAGE3, //white
                "1"
              ]
            ]
          }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#27b0ba",
        "tooltip": Blockly.Msg.BLOCK_OLED_FILL_TOOLTIP,
        "helpUrl": Blockly.Msg.BLOCK_OLED_FILL_HELPURL
      }
    );
  }
};

Blockly.Python['oled_fill'] = function(block) {
  var variable_oled_lcd = Blockly.Python.variableDB_.getName(block.getFieldValue('oled_lcd'), Blockly.Variables.NAME_TYPE);
  var dropdown_color = block.getFieldValue('COLOR');
  // TODO: Assemble Python into code variable.
  //oled.fill(1); oled.show()
  var code = variable_oled_lcd + '.fill(' + dropdown_color + '); ' + variable_oled_lcd + '.show()\n';
  return code;
};

Blockly.Blocks['oled_onoff'] = {
  init: function() {
    this.jsonInit(
      {
        "type": "oled_onoff",
        "message0": Blockly.Msg.BLOCK_OLED_TURN_MESSAGE0,
        "args0": [
          {
            "type": "field_variable",
            "name": "oled_lcd",
            "variable": Blockly.Msg.BLOCK_OLED_TURN_MESSAGE1,
          },
          {
            "type": "field_dropdown",
            "name": "ONOFF",
            "options": [
              [
                Blockly.Msg.BLOCK_OLED_TURN_MESSAGE2,
                "ON"
              ],
              [
                Blockly.Msg.BLOCK_OLED_TURN_MESSAGE3,
                "OFF"
              ]
            ]
          }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": "#27b0ba",
        "tooltip": Blockly.Msg.BLOCK_OLED_TURN_TOOLTIP,
        "helpUrl": Blockly.Msg.BLOCK_OLED_TURN_HELPURL
      }
    );
  }
};

Blockly.Python['oled_onoff'] = function(block) {
  var variable_oled_lcd = Blockly.Python.variableDB_.getName(block.getFieldValue('oled_lcd'), Blockly.Variables.NAME_TYPE);
  var dropdown_onoff = block.getFieldValue('ONOFF');
  // TODO: Assemble Python into code variable.
  //oled.poweroff()
  var code = ''
  if (dropdown_onoff == 'ON') {
    code = variable_oled_lcd + '.poweron()\n';
  } else {
    code = variable_oled_lcd + '.poweroff()\n';
  }

  return code;
};
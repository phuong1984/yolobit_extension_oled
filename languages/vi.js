// Vietnamese language file for Robot Eyes OLED extension
// Tệp ngôn ngữ tiếng Việt cho phần mở rộng Robot Eyes OLED

// ==================================================================
// ROBOT SETUP BLOCK
// ==================================================================
Blockly.Msg.ROBOT_EYES_SETUP_MESSAGE = "🤖 Cài đặt Robot Eyes"
Blockly.Msg.ROBOT_EYES_SETUP_TOOLTIP = "Khởi tạo màn hình OLED"
Blockly.Msg.ROBOT_EYES_SETUP_HELPURL = ""

// ==================================================================
// PLAY ANIMATION BLOCK (BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_PLAY_ANIMATION_MESSAGE = "✨ Chạy %1 Số lần: %2 Tốc độ: %3"
Blockly.Msg.ROBOT_PLAY_ANIMATION_TOOLTIP = "CHẶN: Chạy animation và ĐỢI cho đến khi hoàn thành trước khi tiếp tục. Dùng cho các chuỗi đơn giản. KHÔNG dùng trong vòng lặp 'while True'. CPU bị chặn trong quá trình animation."
Blockly.Msg.ROBOT_PLAY_ANIMATION_HELPURL = ""

// Animation dropdown options
Blockly.Msg.ANIMATION_BLINK = "👁 Nháy mắt"
Blockly.Msg.ANIMATION_LOOK_AROUND = "👀 Nhìn quanh"
Blockly.Msg.ANIMATION_DIZZY = "💫 Choáng váng"
Blockly.Msg.ANIMATION_WAKE_UP = "😴→😊 Thức dậy"
Blockly.Msg.ANIMATION_SHOCKED = "😱 Sốc"
Blockly.Msg.ANIMATION_HAPPY_BOUNCE = "😊 Nhảy vui"
Blockly.Msg.ANIMATION_IDLE = "🔁 Tự động nháy"

// Speed dropdown options
Blockly.Msg.SPEED_NORMAL = "Bình thường (1×)"
Blockly.Msg.SPEED_FAST = "Nhanh (2×)"
Blockly.Msg.SPEED_SLOW = "Chậm (0.5×)"

// ==================================================================
// CREATE ANIMATION BLOCK (NON-BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_MESSAGE = "✨ Tạo Animation (không chặn) %1"
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_TOOLTIP = "KHÔNG CHẶN: Dùng trong vòng lặp 'while True'. Tạo đối tượng animation. Gọi khối update mỗi khung hình. Tốc độ animation phụ thuộc vào time.sleep_ms() trong vòng lặp của bạn (ví dụ: 16ms=nhanh, 100ms=chậm)."
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_HELPURL = ""

// ==================================================================
// UPDATE ANIMATION BLOCK (NON-BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_MESSAGE = "🔄 Cập nhật Animation (không chặn)"
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_TOOLTIP = "Cập nhật một khung hình của animation. Dùng trong vòng lặp 'while True' sau khi tạo animation. Trả về True nếu animation vẫn đang chạy."
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_HELPURL = ""

// ==================================================================
// SHOW SQUARE EXPRESSION BLOCK
// ==================================================================
Blockly.Msg.ROBOT_SHOW_SQUARE_MESSAGE = "⬜ Mắt vuông  Hình dạng: %1  Biểu cảm: %2"
Blockly.Msg.ROBOT_SHOW_SQUARE_TOOLTIP = "Kiểu A: Mắt hình chữ nhật bo tròn. Chọn hình dạng và biểu cảm."
Blockly.Msg.ROBOT_SHOW_SQUARE_HELPURL = ""

// Square shape dropdown options
Blockly.Msg.SQUARE_SHAPE_SHARP = "⬜ Sắc cạnh (rx=4)"
Blockly.Msg.SQUARE_SHAPE_BALANCED = "🔲 Cân bằng (rx=10)"
Blockly.Msg.SQUARE_SHAPE_ROUND = "🔘 Tròn (rx=14)"
Blockly.Msg.SQUARE_SHAPE_WIDE = "▬ Phẳng rộng"

// ==================================================================
// SHOW OVAL EXPRESSION BLOCK
// ==================================================================
Blockly.Msg.ROBOT_SHOW_OVAL_MESSAGE = "👁 Mắt oval  Hình dạng: %1  Biểu cảm: %2"
Blockly.Msg.ROBOT_SHOW_OVAL_TOOLTIP = "Kiểu B: Mắt oval phong cách Oggy. Chọn hình dạng và biểu cảm."
Blockly.Msg.ROBOT_SHOW_OVAL_HELPURL = ""

// Oval shape dropdown options
Blockly.Msg.OVAL_SHAPE_NORMAL = "🔵 Oval bình thường"
Blockly.Msg.OVAL_SHAPE_WIDE = "🏈 Phẳng rộng"
Blockly.Msg.OVAL_SHAPE_TALL = "🥚 Oval cao"
Blockly.Msg.OVAL_SHAPE_BIG = "👁 Bong bóng lớn"

// ==================================================================
// EXPRESSION DROPDOWN OPTIONS (shared for square and oval)
// ==================================================================
Blockly.Msg.EXPR_NORMAL = "😐 Bình thường"
Blockly.Msg.EXPR_HAPPY = "😊 Vui vẻ"
Blockly.Msg.EXPR_SAD = "😢 Buồn"
Blockly.Msg.EXPR_ANGRY = "😠 Giận dữ"
Blockly.Msg.EXPR_SURPRISED = "😲 Ngạc nhiên"
Blockly.Msg.EXPR_SLEEPY = "😴 Buồn ngủ"
Blockly.Msg.EXPR_WINK = "😉 Nháy mắt"
Blockly.Msg.EXPR_LOVE = "😍 Yêu thích"
Blockly.Msg.EXPR_LOOK_LEFT = "👀 Nhìn trái"
Blockly.Msg.EXPR_LOOK_RIGHT = "👀 Nhìn phải"


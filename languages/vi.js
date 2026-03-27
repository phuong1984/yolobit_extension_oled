// Vietnamese language file for Robot Eyes OLED extension
// Tệp ngôn ngữ tiếng Việt cho phần mở rộng Robot Eyes OLED

// ==================================================================
// ROBOT SETUP BLOCK
// ==================================================================
Blockly.Msg.ROBOT_EYES_SETUP_MESSAGE = "🤖 Khởi tạo Robot Eyes"
Blockly.Msg.ROBOT_EYES_SETUP_TOOLTIP = "Khởi tạo Robot Eyes trên màn hình OLED"
Blockly.Msg.ROBOT_EYES_SETUP_HELPURL = ""

// ==================================================================
// PLAY ANIMATION BLOCK (BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_PLAY_ANIMATION_MESSAGE = "✨ Chạy %1 Số lần: %2 Tốc độ: %3"
Blockly.Msg.ROBOT_PLAY_ANIMATION_TOOLTIP = "TỨC THỜI: Chạy diễn hoạt và ĐỢI cho đến khi hoàn thành trước khi tiếp tục. Dùng cho các chuỗi đơn giản. KHÔNG dùng trong vòng lặp 'while True'. CPU bị chặn trong quá trình diễn hoạt."
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
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_MESSAGE = "✨ Tạo diễn hoạt (linh hoạt) %1"
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_TOOLTIP = "LINH HOẠT: Dùng trong vòng lặp 'while True'. Tạo đối tượng diễn hoạt. Gọi khối cập nhật mỗi khung hình. Tốc độ diễn hoạt phụ thuộc vào time.sleep_ms() trong vòng lặp của bạn (ví dụ: 16ms=nhanh, 100ms=chậm)."
Blockly.Msg.ROBOT_CREATE_ANIMATION_NB_HELPURL = ""

// ==================================================================
// UPDATE ANIMATION BLOCK (NON-BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_MESSAGE = "🔄 Cập nhật diễn hoạt (linh hoạt)"
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_TOOLTIP = "Cập nhật một khung hình của diễn hoạt. Dùng trong vòng lặp 'while True' sau khi tạo diễn hoạt. Trả về True nếu diễn hoạt vẫn đang chạy."
Blockly.Msg.ROBOT_UPDATE_ANIMATION_NB_HELPURL = ""

// ==================================================================
// SHOW SQUARE EXPRESSION BLOCK
// ==================================================================
Blockly.Msg.ROBOT_SHOW_SQUARE_MESSAGE = "⬜ Mắt vuông  Dạng nền: %1  Biểu cảm: %2"
Blockly.Msg.ROBOT_SHOW_SQUARE_TOOLTIP = "Kiểu A: Mắt hình chữ nhật bo tròn. Chọn hình dạng nền và biểu cảm."
Blockly.Msg.ROBOT_SHOW_SQUARE_HELPURL = ""

// Square shape dropdown options
Blockly.Msg.SQUARE_SHAPE_SHARP = "⬜ Sắc cạnh (rx=4)"
Blockly.Msg.SQUARE_SHAPE_BALANCED = "🔲 Cân bằng (rx=10)"
Blockly.Msg.SQUARE_SHAPE_ROUND = "🔘 Tròn (rx=14)"
Blockly.Msg.SQUARE_SHAPE_WIDE = "▬ Phẳng rộng"

// ==================================================================
// SHOW OVAL EXPRESSION BLOCK
// ==================================================================
Blockly.Msg.ROBOT_SHOW_OVAL_MESSAGE = "👁 Mắt oval  Dạng nền: %1  Biểu cảm: %2"
Blockly.Msg.ROBOT_SHOW_OVAL_TOOLTIP = "Kiểu B: Mắt oval phong cách Oggy. Chọn hình dạng nền và biểu cảm."
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
Blockly.Msg.EXPR_LOVE = "😍 Đang yêu"
Blockly.Msg.EXPR_LOOK_LEFT = "👀 Nhìn trái"
Blockly.Msg.EXPR_LOOK_RIGHT = "👀 Nhìn phải"

// ==================================================================
// Custom expression block
// ==================================================================
Blockly.Msg.ROBOT_SHOW_CUSTOM_MESSAGE =
    "Mắt tùy chỉnh  Biểu cảm: %1  Chiều rộng mắt: %2 px  Chiều cao mắt: %3 px  Bán kính góc: %4 px  Con ngươi: %5";

Blockly.Msg.PUPIL_SMALL  = "nhỏ";
Blockly.Msg.PUPIL_MEDIUM = "vừa";
Blockly.Msg.PUPIL_LARGE  = "to";

Blockly.Msg.ROBOT_SHOW_CUSTOM_TOOLTIP =
    "Hiển thị biểu cảm với hình dạng mắt tùy chỉnh. " +
    "Chiều rộng: 10–56 px, Chiều cao: 10–40 px, " +
    "Bo góc: 0 (sắc cạnh) đến min(w,h)/2 (hình viên thuốc). " +
    "Bán kính bo góc tự động giới hạn nếu nhập quá lớn. " +
    "Kích thước con ngươi tự động điều chỉnh theo chiều rộng mắt.";
Blockly.Msg.ROBOT_SHOW_CUSTOM_HELPURL = "";

// ==================================================================
// ANIMATE CUSTOM EYES (NON-BLOCKING)
// ==================================================================
Blockly.Msg.ROBOT_ANIMATE_CUSTOM_MESSAGE = "🎬 Diễn hoạt mắt tùy chỉnh %1";

Blockly.Msg.ANIMATE_MODE_IDLE = "rảnh rỗi (đứng yên)";
Blockly.Msg.ANIMATE_MODE_MOVE = "di chuyển (đi quanh)";
Blockly.Msg.ANIMATE_MODE_ACTION = "hành động (đặc trưng)";
Blockly.Msg.ANIMATE_MODE_ALL = "tất cả (chu kỳ: rảnh rỗi → di chuyển → hành động)";

Blockly.Msg.ROBOT_ANIMATE_CUSTOM_TOOLTIP =
    "LINH HOẠT: Diễn hoạt mắt tùy chỉnh theo biểu cảm. " +
    "rảnh rỗi: Đứng yên với diễn hoạt đặc trưng của biểu cảm. " +
    "di chuyển: Đi quanh màn hình với phong cách đặc trưng. " +
    "hành động: Thực hiện hành động đặc trưng của biểu cảm. " +
    "tất cả: Chu kỳ rảnh rỗi (2s) → di chuyển (3s) → hành động → lặp lại. " +
    "Cần khởi tạo mắt tùy chỉnh trước khi sử dụng." +
    "Dùng trong vòng lặp 'while True'. Gọi liên tục mỗi khung hình.";
Blockly.Msg.ROBOT_ANIMATE_CUSTOM_HELPURL = "";
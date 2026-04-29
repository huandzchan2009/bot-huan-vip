const TelegramBot = require('node-telegram-bot-api');

// Token bạn vừa cung cấp
const token = '8613218758:AAGpN9S6xJnQhSQ21FG4BzERNp5-RbTC6BY';
const bot = new TelegramBot(token, {polling: true});

const GAME_URL = "https://sunwin.ml/"; // Link game của bạn

console.log("--- TOOLVIPPRO BOT IS RUNNING ---");

// Giao diện khi người dùng gõ /start
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const firstName = msg.from.first_name;

    const message = `
🔥 **CHÀO MỪNG ${firstName.toUpperCase()} ĐẾN VỚI TOOLVIPPRO** 🔥
━━━━━━━━━━━━━━━━━━━━━━━━
🤖 **Hệ thống:** AI Auto Predict Pro Max
✨ **Phiên bản:** 2.4 (Sunwin Edition)
💎 **Trạng thái:** [ Hoạt động tốt ✅ ]

⚡ *Vui lòng chọn các tính năng bên dưới để bắt đầu soi cầu!*
    `;

    const options = {
        parse_mode: 'Markdown',
        reply_markup: {
            inline_keyboard: [
                [
                    { text: '🎮 VÀO GAME NGAY (CHƠI TRÊN WEB)', url: GAME_URL }
                ],
                [
                    { text: '📱 MỞ TOOL TRONG TELEGRAM', web_app: { url: GAME_URL } }
                ],
                [
                    { text: '📖 Hướng dẫn cài đặt', callback_data: 'guide' },
                    { text: '🛠 Hỗ trợ kỹ thuật', callback_data: 'support' }
                ],
                [
                    { text: '🌍 Trang chủ ToolHDX', url: 'https://toolhdx.site/' }
                ]
            ]
        }
    };

    bot.sendMessage(chatId, message, options);
});

// Xử lý các nút bấm phản hồi (Callback)
bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;
    const data = query.data;

    if (data === 'guide') {
        const guideText = `
📖 **HƯỚNG DẪN CÀI ĐẶT NHANH:**

1️⃣ **Android:** Cài trình duyệt **Kiwi Browser**, thêm tiện ích **Tampermonkey**, sau đó dán Script \`toolvippro\`.
2️⃣ **PC:** Cài tiện ích **Tampermonkey** trực tiếp trên Chrome/Edge.
3️⃣ **iOS:** Cài ứng dụng **Userscripts** trên App Store.

*Sau khi cài xong, bạn chỉ cần bấm nút "Vào Game" bên trên là Tool tự hiện!*
        `;
        bot.sendMessage(chatId, guideText, { parse_mode: 'Markdown' });
    }

    if (data === 'support') {
        bot.sendMessage(chatId, "🛠 **HỖ TRỢ KỸ THUẬT:**\n\nNếu gặp lỗi không hiện Tool, vui lòng liên hệ Admin: @HuyDaiXu_AI", { parse_mode: 'Markdown' });
    }

    // Xóa trạng thái loading trên nút bấm
    bot.answerCallbackQuery(query.id);
});

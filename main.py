import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import time
import datetime
import os
from flask import Flask
from threading import Thread

# --- CẤU HÌNH ---
TOKEN = "8613218758:AAGpN9S6xJnQhSQ21FG4BzERNp5-RbTC6BY"
LINK_DICH = "https://link4m.com/Kxz7nMs"
KEY_MO_KHOA = "HUAN2604"
ID_ADMIN_VIP = [8514251389,7945857847] # ID của bạn

bot = telebot.TeleBot(TOKEN)
user_usage = {}

# --- KEEP ALIVE (Dành cho Render/Replit) ---
app = Flask('')
@app.route('/')
def home(): return "Bot Admin Huân đang chạy!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# --- RESET LƯỢT DÙNG MỖI NGÀY ---
def check_user(uid):
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    if uid not in user_usage or user_usage[uid].get('date') != today:
        user_usage[uid] = {'total': 0, 'limit': 5, 'date': today}

# --- MENU CHÍNH ---
def get_main_menu():
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("🎯 Lấy Acc", callback_data="get_acc"),
        InlineKeyboardButton("🔗 Lấy Key (15 Lượt)", url=LINK_DICH)
    )
    kb.row(
        InlineKeyboardButton("🔑 Nhập Key", callback_data="input_key"),
        InlineKeyboardButton("👑 Nâng Cấp VIP", callback_data="buy_vip")
    )
    return kb

# --- LỆNH /START ---
@bot.message_handler(commands=['start'])
def send_welcome(m):
    uid = m.chat.id
    check_user(uid)
    status = "👑 Thành viên PREMIUM" if uid in ID_ADMIN_VIP else "👤 Thành viên thường"
    
    welcome_text = f"""
🌟 *HỆ THỐNG SCAN ACC LIÊN QUÂN - ADMIN HUÂN* 🌟
━━━━━━━━━━━━━━━━━━━

📱 Trạng thái: {status}
🆔 ID của bạn: `{uid}`

🎁 *CHẾ ĐỘ MIỄN PHÍ:*
✅ Tặng 5 Acc FREE đầu tiên.
🔗 Hết lượt bot tự gửi link để lấy thêm 10 Acc (Không giới hạn).

👑 *ĐẶC QUYỀN PREMIUM (50k):*
🎯 Tỉ lệ trúng Skin SS, Tuyệt Sắc cực cao.
🛡️ Acc sạch, cam kết không bay màu.
🚀 Scan không giới hạn - Không chờ - Không vượt link.

━━━━━━━━━━━━━━━━━━━

📞 LIÊN HỆ MUA PREMIUM TẠI:
✈️ Telegram: @huansbotvip
📱 Zalo: 0354714903

👉 *NHẬP SỐ LƯỢNG ACC MUỐN LẤY:*
"""
    bot.send_message(uid, welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())

# --- XỬ LÝ NÚT BẤM ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    uid = call.message.chat.id
    if call.data == "get_acc":
        bot.send_message(uid, "📥 Hãy gửi số lượng acc bạn muốn lấy (Ví dụ: 5)")
    elif call.data == "input_key":
        bot.send_message(uid, "🔑 Hãy dán mã KEY bạn nhận được từ link vào đây để kích hoạt 15 lượt:")
    elif call.data == "buy_vip":
        bot.send_message(uid, "👑 Liên hệ nâng cấp: @huansbotvip hoặc Zalo: 0354714903")

# --- XỬ LÝ TIN NHẮN (LẤY ACC/NHẬP KEY) ---
@bot.message_handler(func=lambda m: True)
def handle_text(m):
    uid = m.chat.id
    text = m.text.strip()
    check_user(uid)

    # Nhập Key mở khóa
    if text.upper() == KEY_MO_KHOA:
        user_usage[uid]['limit'] = 15
        bot.send_message(uid, "🔓 Xác thực thành công! Bạn có 15 lượt cho hôm nay.")
        return

    # Nhập số lượng lấy acc
    try:
        qty = int(text)
    except ValueError:
        return

    if qty > 10: qty = 10
    if qty <= 0: return

    # Kiểm tra lượt dùng
    if uid not in ID_ADMIN_VIP and user_usage[uid]['total'] >= user_usage[uid]['limit']:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔗 Vượt link lấy mã KEY", url=LINK_DICH))
        msg = "❌ Bạn đã hết lượt miễn phí! Vượt link bên dưới để nhận KEY nâng cấp lên 15 lượt."
        bot.send_message(uid, msg, reply_markup=markup)
        return

    bot.send_message(uid, f"🚀 Đang quét {qty} tài khoản...")
    for i in range(qty):
        try:
            res = requests.get("https://keyherlyswar.x10.mx/Apidocs/reg/reglq.php", timeout=10).json()
            if res.get("status") and res.get("result"):
                if uid not in ID_ADMIN_VIP:
                    user_usage[uid]['total'] += 1
                acc_info = f"{res['result'][0]['account']}|{res['result'][0]['password']}"
                bot.send_message(uid, f"✅ STT {i+1}: `{acc_info}`", parse_mode="Markdown")
            else:
                bot.send_message(uid, "❌ Kho acc hiện tại đang trống.")
                break
        except:
            bot.send_message(uid, "❌ Lỗi kết nối API.")
            break
        time.sleep(0.5)

# --- CHẠY ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import time
import datetime
import os
from flask import Flask
from threading import Thread
import urllib3

# Tắt cảnh báo SSL không an toàn để tránh làm bẩn nhật ký log
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CẤU HÌNH ---
TOKEN = "8613218758:AAGpN9S6xJnQhSQ21FG4BzERNp5-RbTC6BY"
LINK_DICH = "https://fnote.net/notes/2QsYGR"
KEY_MO_KHOA = "HUAN2604"
ID_ADMIN_VIP = [8514251389] 

bot = telebot.TeleBot(TOKEN)
user_usage = {}

# --- KEEP ALIVE ---
app = Flask('')
@app.route('/')
def home():
    return "Bot Admin Huân đang chạy!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

def check_user(uid):
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    if uid not in user_usage or user_usage[uid].get('date') != today:
        user_usage[uid] = {'total': 0, 'limit': 5, 'date': today}

def get_main_menu():
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("🎯 Lấy Acc", callback_data="get_acc"),
        InlineKeyboardButton("🔗 Lấy Key (Thêm 10 Lượt)", url=LINK_DICH)
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
    congrats_vip = "🎊 *CHÚC MỪNG!* Bạn đang sở hữu đặc quyền *VIP* vĩnh viễn! 🎊\n\n" if uid in ID_ADMIN_VIP else ""
    
    welcome_text = congrats_vip + f"""
🌟 *HỆ THỐNG SCAN ACC LIÊN QUÂN - ADMIN HUÂN* 🌟
━━━━━━━━━━━━━━━━━━━

📱 Trạng thái: {status}
🆔 ID của bạn: `{uid}`

🎁 *CHẾ ĐỘ MIỄN PHÍ:*
✅ Tặng 5 Acc FREE mỗi ngày.
🔗 Nhập KEY để nhận thêm 10 lượt dùng (Tổng 15).

👑 *ĐẶC QUYỀN PREMIUM (50k):*
🎯 Skin SS, Tuyệt Sắc cực cao.
🚀 Scan không giới hạn - Không chờ - Không vượt link.

━━━━━━━━━━━━━━━━━━━
📞 Liên hệ: @huansbotvip | Zalo: 0354714903
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
        bot.send_message(uid, "🔑 Hãy dán mã KEY bạn nhận được từ link vào đây để kích hoạt 10 lượt:")
    elif call.data == "buy_vip":
        bot.send_message(uid, "👑 Liên hệ nâng cấp: @huansbotvip")

# --- XỬ LÝ TIN NHẮN ---
@bot.message_handler(func=lambda m: True)
def handle_text(m):
    uid = m.chat.id
    text = m.text.strip()
    check_user(uid)

    if text.upper() == KEY_MO_KHOA:
        user_usage[uid]['limit'] = 15 
        bot.send_message(uid, "🔓 Xác thực thành công! Bạn có thêm 10 lượt (Tổng 15 lượt) cho hôm nay.")
        return

    try:
        qty = int(text)
    except ValueError: return

    if qty > 10: qty = 10
    if qty <= 0: return

    if uid not in ID_ADMIN_VIP and user_usage[uid]['total'] >= user_usage[uid]['limit']:
        markup = InlineKeyboardMarkup()
        if user_usage[uid]['limit'] == 5:
            markup.add(InlineKeyboardButton("🚀 LẤY MÃ KEY NHẬN 10 LƯỢT", url=LINK_DICH))
            bot.send_message(uid, "❌ Hết lượt free! Nhấn nút dưới đây để nhận thêm 10 lượt:", reply_markup=markup)
        else:
            bot.send_message(uid, "🚫 Bạn đã đạt giới hạn 15 lượt hôm nay! Vui lòng mua VIP hoặc đợi đến 12h trưa mai.")
        return

    msg_scan = "🚀 *VIP ĐANG QUÉT...*" if uid in ID_ADMIN_VIP else f"🚀 Đang quét {qty} tài khoản..."
    bot.send_message(uid, msg_scan, parse_mode="Markdown")

    for i in range(qty):
        if uid not in ID_ADMIN_VIP and user_usage[uid]['total'] >= user_usage[uid]['limit']:
            bot.send_message(uid, "⚠️ Đã dừng quét vì bạn vừa dùng hết lượt free!")
            break

        try:
            # Sửa lỗi API: Thêm verify=False và kiểm tra dữ liệu phản hồi
            response = requests.get("https://keyherlyswar.x10.mx/Apidocs/reg/reglq.php", timeout=10, verify=False)
            if response.status_code == 200:
                res = response.json()
                if res.get("status") and "result" in res and len(res["result"]) > 0:
                    if uid not in ID_ADMIN_VIP:
                        user_usage[uid]['total'] += 1
                    
                    acc_data = res['result'][0]
                    acc_info = f"{acc_data['account']}|{acc_data['password']}"
                    prefix = f"✨ VIP {i+1}" if uid in ID_ADMIN_VIP else f"✅ STT {i+1}"
                    bot.send_message(uid, f"{prefix}: `{acc_info}`", parse_mode="Markdown")
                else:
                    bot.send_message(uid, "❌ Kho acc trống.")
                    break
            else:
                bot.send_message(uid, f"❌ Lỗi API (Mã: {response.status_code}).")
                break
        except Exception:
            bot.send_message(uid, "❌ Lỗi kết nối API.")
            break
        time.sleep(0.8) # Nghỉ một chút để tránh bị API chặn vì yêu cầu quá nhanh

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

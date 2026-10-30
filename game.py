import json
from config import *

# 🎮 متغیر نگهداری وضعیت بازی‌ها
games = {}

def get_board_keyboard(board):
    keyboard = []
    for i in range(0, 16, 4):
        row = []
        for j in range(4):
            idx = i + j
            text = board[idx] if board[idx] != "" else "⬜"
            row.append({"text": text, "callback_data": f"doz_{idx}"})
        keyboard.append(row)
    return json.dumps({"inline_keyboard": keyboard})

def check_winner(board, player):
    for i in range(4):
        if all(board[i*4 + j] == player for j in range(4)): return True
    for j in range(4):
        if all(board[i*4 + j] == player for i in range(4)): return True
    if all(board[i*4 + i] == player for i in range(4)): return True
    if all(board[i*4 + (3-i)] == player for i in range(4)): return True
    return False

# 🚪 تابع بررسی گپ غیرمجاز و خروج خودکار
def check_and_leave_unauthorized(chat_id, bot_id):
    # اگه گپ توی لیست مجاز نبود
    if str(chat_id) not in ALLOWED_CHATS:
        # اگه ربات به عنوان ادمین یا عضو جدید اضافه شده بود، خودش رو خارج کن
        leave_url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/leaveChat"
        data = json.dumps({"chat_id": chat_id}).encode('utf-8')
        req = urllib.request.Request(leave_url, data=data, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
            print(f"⚠️ ربات از گپ غیرمجاز {chat_id} خارج شد.")
        except Exception as e:
            print(f"❌ خطا در خروج از گپ {chat_id}: {e}")
        return True
    return False

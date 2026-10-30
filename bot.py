import urllib.request
import json
import uuid
import time
import os
from datetime import datetime, timezone, timedelta

# 🔐 خواندن توکن از محیط سرور
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
if not BOT_TOKEN:
    print("❌ خطا: توکن ربات تنظیم نشده است!")
    exit()

# 🎯 آیدی عددی گپ‌ها
CHAT_ID_SAMBAH_B = '4884670320'
CHAT_ID_ETTELA_B = '5900955714'
CHAT_ID_SAMBAH_A = '4652272518'
CHAT_ID_ETTELA_A = '4491248758'
CHAT_ID_HAMALAT = '5681028578'
CHAT_ID_DOORHAMI = '6023524639'
CHAT_ID_VORUDI = '5559869385'
CHAT_ID_AMIRALI = '4853834278'
CHAT_ID_MAJID = '5422739931'
CHAT_ID_TITAP = '5562715565'
CHAT_ID_GAMES = '5562715565' 

BLOCKED_ROBOTS = ['940993529']

CHATS_INFO = {
    CHAT_ID_SAMBAH_B: "𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐆𝐓 (𝐁)",
    CHAT_ID_ETTELA_B: "𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐍𝐞𝐰𝐬🔔 (𝐁)",
    CHAT_ID_SAMBAH_A: "𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐆𝐓 (𝐀)",
    CHAT_ID_ETTELA_A: "𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐍𝐞𝐰𝐬🔔 (𝐀)",
    CHAT_ID_HAMALAT: "⚔️𝐒𝐚𝐦𝐛𝐚𝐡 𝐀𝐭𝐭𝐚𝐜𝐤𝐬⚔️",
    CHAT_ID_DOORHAMI: "🎊𝗦𝗮𝗺𝗯𝗮𝗵 𝗚𝗮𝗺𝗲𝘀🎊",
    CHAT_ID_VORUDI: "🚷𝗦𝗮𝗺𝗯𝗮 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆🚷",
    CHAT_ID_AMIRALI: "𝐀𝐦𝐢𝐫𝐀𝐥𝐢 𝐂𝐡𝐚𝐭",
    CHAT_ID_MAJID: "𝐌𝐚𝐣𝐢𝐝 𝐂𝐡𝐚𝐭",
    CHAT_ID_TITAP: "𝐓𝐢𝐭𝐚𝐩 𝐂𝐡𝐚𝐭"
}

ALLOWED_CHATS = list(CHATS_INFO.keys())
BOT_ADMINS = ['724704269', '566594483', '2065233217']

# لینک‌های پشتیبان
FALLBACK_LINK_SAMBAH_B = "https://ble.ir/join/4F2HQJ3rpD"
FALLBACK_LINK_ETTELA_B = "https://ble.ir/join/4zejnKnWu5"
FALLBACK_LINK_SAMBAH_A = "https://ble.ir/join/83tUiWjnM7"
FALLBACK_LINK_ETTELA_A = "https://ble.ir/join/"
FALLBACK_LINK_HAMALAT = "https://ble.ir/join/JA8nUskQGD"
FALLBACK_LINK_DOORHAMI = "https://ble.ir/join/8wN5aYsMf2"
FALLBACK_LINK_VORUDI = "https://ble.ir/join/2ECrbAhGsE"
FALLBACK_LINK_AMIRALI = "https://ble.ir/join/AvWobZ1w2R"
FALLBACK_LINK_MAJID = "https://ble.ir/join/2PvmzANtGf"
FALLBACK_LINK_TITAP = "https://ble.ir/join/CaKiHc9jYm"

current_links = {
    CHAT_ID_SAMBAH_B: FALLBACK_LINK_SAMBAH_B,
    CHAT_ID_ETTELA_B: FALLBACK_LINK_ETTELA_B,
    CHAT_ID_SAMBAH_A: FALLBACK_LINK_SAMBAH_A,
    CHAT_ID_ETTELA_A: FALLBACK_LINK_ETTELA_A,
    CHAT_ID_HAMALAT: FALLBACK_LINK_HAMALAT,
    CHAT_ID_DOORHAMI: FALLBACK_LINK_DOORHAMI,
    CHAT_ID_VORUDI: FALLBACK_LINK_VORUDI,
    CHAT_ID_AMIRALI: FALLBACK_LINK_AMIRALI,
    CHAT_ID_MAJID: FALLBACK_LINK_MAJID,
    CHAT_ID_TITAP: FALLBACK_LINK_TITAP
}

VIDEO_CACHE_FILE = 'welcome_video.txt'
USERS_DB_FILE = 'users_data.json'
BANNED_USERS_FILE = 'banned_users.json'

LINKS_LOCKED = False

PV_WELCOME_TEXT = """درود ✨
کلن بزرگ 𓄂SAMBAH𓆃 عضو گیری میکند 
«*سمباح:سازمان مبارزه با بی اخلاقی و بی حیایی* »
مهم نیست امروز شروع کرده باشی در هر سطحی هر لولی حتی تازه کارترین هارو قوی میکنیم 🚀

💸آموزش برداشت خودکار معدن
💹قوی کردن اکانت 
🔮رسیدن به کریستال 
✨برای عضویت و سوالات درباره کلن به دکمه‌های زیر مراجعه کنید:"""

caption_template = """درود {name} ✨
اگه تو واحد B هستی حتما یکی از سلاطینی🙌

*قوانین کلن بزرگ سمباح واحد B*

*1_* تگ سمباح رو حتما روی اسمتون بزارید به این صورت  𓄂Name𓆃 
(ترجیحا اسم انگلیسی باشه)

*2_* از فحاشی کردن به همدیگه یا به افراد دیگه در کلن های دیگه به خصوص *فحش ناموسی* خودداری کنید

*3_* هیچ کس حق درخواست ادمینی نداره هرکس صلاح باشه خودمون ادمین میکنیم 

*4_* هیچ گپی بدون اجازه ادمین ها نمیرید که ازتون پیام بگیرن چ همچنان در دیدگاه کانالی هم که نمیشناسید پیام نمیدید 

*5_* حق بی احترامی به ادمین هارو ندارید 

*6_* برداشت خودکار معدن که اموزشش گذاشته شده اجباریه و همه باید تنظیم کنن کار سختی هم نیست اگر نشد بله خودتونو بروز کنید  

*7_* به هیچ وجه نبینم کسی برای سکه یا رنک هم کلنی _بدون اجازه _ بزنه اگه اینکارو کرد بهتره قبل از اینکه کیک شه بره

*8_* اگه تو گپی از دشمنی پیام گرفتید باید کیکش کنید مالکیت گپ رو به لیدرا بدید 

*9_* گروهایی که شما باید عضو باشید یکی اطلاع رسانی و یکی گپ سمباح هستش و دورهمی سمباح که اجباری نیستش و همه باید تو ورودی پیام گذاشته باشن 

*10_* هیچکس حق دادن هیچ‌گونه اطلاعاتی از کلن نداره بخصوص لینک دادن و هیچ عضوی بدون اجازه نمیارید هرکس مدنظر بود به ادمینا اطلاع بدید

اگه خوندید و قبول دارید بنویسید قبول دارم ✅
خوش بگذرونید🚀"""

admin_states = {}
games = {}

def load_banned_users():
    if os.path.exists(BANNED_USERS_FILE):
        with open(BANNED_USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_banned_users(banned_list):
    with open(BANNED_USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(banned_list, f)

def is_banned(user_id):
    return str(user_id) in load_banned_users()

def ban_user(user_id):
    banned = load_banned_users()
    if str(user_id) not in banned:
        banned.append(str(user_id))
        save_banned_users(banned)

def unban_user(user_id):
    banned = load_banned_users()
    if str(user_id) in banned:
        banned.remove(str(user_id))
        save_banned_users(banned)

def save_user_data(user_id, user_name):
    users = {}
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
            try:
                users = json.load(f)
            except:
                users = {}
    users[str(user_id)] = user_name
    with open(USERS_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def is_link_time_blocked():
    iran_tz = timezone(timedelta(hours=3, minutes=30))
    now = datetime.now(iran_tz)
    hour = now.hour
    if hour >= 23 or hour < 10:
        return True
    return False

def send_request(method, data=None):
    url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/{method}"
    if data:
        data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    else:
        req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"ok": False, "error": str(e)}

def is_admin(chat_id, user_id):
    if str(user_id) in BOT_ADMINS: return True
    res = send_request("getChatMember", {"chat_id": chat_id, "user_id": user_id})
    if res.get("ok") and res["result"].get("status") in ["creator", "administrator"]:
        return True
    return False

def get_link(chat_id):
    res = send_request("exportChatInviteLink", {"chat_id": chat_id})
    if res.get("ok"):
        current_links[chat_id] = res["result"]
        return res["result"]
    return current_links.get(chat_id, "https://ble.ir/")

def get_welcome_keyboard():
    if LINKS_LOCKED or is_link_time_blocked():
        return json.dumps({"inline_keyboard": []})
    return json.dumps({
        "inline_keyboard": [
            [{"text": '💬 𝐒𝐚𝐦𝐛𝐚𝐡 𝐆𝐓 (𝐁)', "url": get_link(CHAT_ID_SAMBAH_B)}],
            [{"text": '🔔 𝐒𝐚𝐦𝐛𝐚𝐡 𝐍𝐞𝐰𝐬 (𝐁)', "url": get_link(CHAT_ID_ETTELA_B)}],
            [{"text": '⚔️ 𝐒𝐚𝐦𝐛𝐚𝐡 𝐀𝐭𝐭𝐚𝐜𝐤𝐬', "url": get_link(CHAT_ID_HAMALAT)}],
            [{"text": '🎊 𝐒𝐚𝐦𝐛𝐚𝐡 𝐆𝐚𝐦𝐞𝐬', "url": get_link(CHAT_ID_DOORHAMI)}]
        ]
    }, ensure_ascii=False)

def get_links_keyboard():
    return json.dumps({
        "inline_keyboard": [
            [{"text": '𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐆𝐓 (𝐁)', "url": get_link(CHAT_ID_SAMBAH_B)}],
            [{"text": '𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐍𝐞𝐰𝐬🔔 (𝐁)', "url": get_link(CHAT_ID_ETTELA_B)}],
            [{"text": '𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐆𝐓 (𝐀)', "url": get_link(CHAT_ID_SAMBAH_A)}],
            [{"text": '𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐍𝐞𝐰𝐬🔔 (𝐀)', "url": get_link(CHAT_ID_ETTELA_A)}],
            [{"text": '⚔️𝐒𝐚𝐦𝐛𝐚𝐡 𝐀𝐭𝐭𝐚𝐜𝐤𝐬⚔️', "url": get_link(CHAT_ID_HAMALAT)}],
            [{"text": '🎊𝗦𝗮𝗺𝗯𝗮𝗵 𝗚𝗮𝗺𝗲𝘀🎊', "url": get_link(CHAT_ID_DOORHAMI)}],
            [{"text": '🚷𝗦𝗮𝗺𝗯𝗮 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆🚷', "url": get_link(CHAT_ID_VORUDI)}],
            [{"text": '𝐀𝐦𝐢𝐫𝐀𝐥𝐢 𝐂𝐡𝐚𝐭', "url": get_link(CHAT_ID_AMIRALI)}],
            [{"text": '𝐌𝐚𝐣𝐢𝐝 𝐂𝐡𝐚𝐭', "url": get_link(CHAT_ID_MAJID)}],
            [{"text": '𝐓𝐢𝐭𝐚𝐩 𝐂𝐡𝐚𝐭', "url": get_link(CHAT_ID_TITAP)}]
        ]
    }, ensure_ascii=False)

def get_pv_keyboard():
    return json.dumps({
        "inline_keyboard": [
            [{"text": '🎮 ربات بازی (StarWar)', "url": "https://ble.ir/StarWarFrg_RoBot"}],
            [{"text": '📩 جهت عضویت در کلن پیام دهید (۱)', "url": "https://ble.ir/SAMBAHY"}],
            [{"text": '📩 جهت عضویت در کلن پیام دهید (۲)', "url": "https://ble.ir/mmdrza168"}]
        ]
    }, ensure_ascii=False)

def send_video_to_target(video_file_id, user_name="دوست عزیز"):
    url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendVideo"
    boundary = uuid.uuid4().hex
    body = b''
    fields = {
        'chat_id': CHAT_ID_SAMBAH_B,
        'video': video_file_id,
        'caption': caption_template.format(name=user_name),
        'parse_mode': 'Markdown',
        'reply_markup': get_welcome_keyboard()
    }
    for key, value in fields.items():
        body += f'--{boundary}\r\n'.encode('utf-8')
        body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8')
        body += f'{value}\r\n'.encode('utf-8')
    body += f'--{boundary}--\r\n'.encode('utf-8')
    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"ok": False, "error": str(e)}

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

saved_video_id = None
if os.path.exists(VIDEO_CACHE_FILE):
    with open(VIDEO_CACHE_FILE, 'r') as f:
        saved_video_id = f.read().strip()

print("⏳ در حال پاکسازی...")
updates = send_request("getUpdates", {"offset": -1})
if updates.get("ok") and updates.get("result"):
    last_update_id = updates["result"][-1]["update_id"]
    send_request("getUpdates", {"offset": last_update_id + 1, "limit": 1})
else:
    last_update_id = 0

print("\n🤖 ربات روشن شد...")

while True:
    try:
        updates = send_request("getUpdates", {"offset": last_update_id + 1, "timeout": 0})
        
        if updates.get("ok") and updates.get("result"):
            for update in updates["result"]:
                last_update_id = update["update_id"]
                
                if "message" in update:
                    msg = update["message"]
                    chat_id = str(msg["chat"]["id"])
                    user_id = str(msg["from"]["id"])
                    user_name = msg["from"].get("first_name", "Player")
                    
                    if user_id in BLOCKED_ROBOTS or msg.get("from", {}).get("is_bot"):
                        continue

                    if is_banned(user_id):
                        if chat_id == user_id:
                            send_request("sendMessage", {"chat_id": chat_id, "text": "🚫 **شما از ربات بن شده‌اید!**", "reply_markup": json.dumps({"inline_keyboard": [[{"text": "📩 درخواست لغو بن", "callback_data": "unban_request"}]]})})
                        continue

                    if not msg.get("from", {}).get("is_bot"):
                        save_user_data(user_id, user_name)
                    
                    if "text" in msg and msg["text"].strip() == 'دوز':
                        if "reply_to_message" in msg:
                            target_id = str(msg["reply_to_message"]["from"]["id"])
                            target_name = msg["reply_to_message"]["from"].get("first_name", "Player")
                            if target_id == user_id or target_id in BLOCKED_ROBOTS: continue
                            games[chat_id] = {'board': [""] * 16, 'turn': '❌', 'p1': user_id, 'p2': target_id, 'p1_name': user_name, 'p2_name': target_name, 'active': True}
                            send_request("sendMessage", {"chat_id": chat_id, "text": f"🎮 **بازی دوز شروع شد!**\n\n❌ {user_name}\n⭕️ {target_name}", "reply_markup": get_board_keyboard(games[chat_id]['board'])})
                            continue

                    if chat_id == user_id:
                        if user_id not in BOT_ADMINS:
                            if "text" in msg and msg["text"].strip() == '/start':
                                send_request("sendMessage", {"chat_id": chat_id, "text": PV_WELCOME_TEXT, "reply_markup": get_pv_keyboard()})
                            continue 
                        
                        if "text" in msg and msg["text"].strip() in ['/start', 'پنل', '/panel']:
                            kb = json.dumps({
                                "inline_keyboard": [
                                    [{"text": "📢 ارسال پیام سراسری", "callback_data": "admin_broadcast"}],
                                    [{"text": "🎬 تغییر فیلم خوش‌آمدگویی", "callback_data": "change_video"}],
                                    [{"text": "🔒 قفل کردن لینک‌ها", "callback_data": "lock_links"}],
                                    [{"text": "🔓 باز کردن لینک‌ها", "callback_data": "unlock_links"}],
                                    [{"text": "🦉 پیدا کردن جغدها", "callback_data": "find_owls"}],
                                    [{"text": "🚫 بن کردن کاربر", "callback_data": "admin_ban"}],
                                    [{"text": "✅ آنبن کردن کاربر", "callback_data": "admin_unban"}],
                                    [{"text": "📋 لیست کاربران بن شده", "callback_data": "list_banned"}]
                                ]
                            }, ensure_ascii=False)
                            send_request("sendMessage", {"chat_id": chat_id, "text": "👑 **پنل مدیریت**\nخوش آمدید ادمین عزیز.", "reply_markup": kb, "parse_mode": "Markdown"})
                            continue

                    if user_id in admin_states:
                        state = admin_states[user_id]
                        
                        if state['step'] == 'waiting_for_ban_id' and 'text' in msg:
                            target_id = msg['text'].strip()
                            ban_user(target_id)
                            send_request("sendMessage", {"chat_id": chat_id, "text": f"🚫 کاربر با آیدی `{target_id}` بن شد.", "parse_mode": "Markdown"})
                            del admin_states[user_id]
                            continue
                            
                        if state['step'] == 'waiting_for_unban_id' and 'text' in msg:
                            target_id = msg['text'].strip()
                            unban_user(target_id)
                            send_request("sendMessage", {"chat_id": chat_id, "text": f"✅ کاربر با آیدی `{target_id}` آنبن شد.", "parse_mode": "Markdown"})
                            del admin_states[user_id]
                            continue

                        if state['step'] == 'waiting_for_video':
                            if "video" in msg:
                                with open(VIDEO_CACHE_FILE, 'w') as f:
                                    f.write(msg["video"]["file_id"])
                                saved_video_id = msg["video"]["file_id"]
                                send_request("sendMessage", {"chat_id": chat_id, "text": "✅ **فیلم ذخیره شد.**"})
                            else:
                                send_request("sendMessage", {"chat_id": chat_id, "text": "❌ لطفاً **فیلم** بفرستید."})
                            del admin_states[user_id]
                            continue

                        if state['step'] == 'get_text' and state['target'] == 'pv' and 'text' in msg:
                            if os.path.exists(USERS_DB_FILE):
                                with open(USERS_DB_FILE, 'r') as f:
                                    all_users = list(json.load(f).keys())
                                count = 0
                                for uid in all_users:
                                    res = send_request("sendMessage", {"chat_id": uid, "text": f"📢 [سراسری]\n\n{msg['text']}"})
                                    if res.get("ok"): count += 1
                                send_request("sendMessage", {"chat_id": chat_id, "text": f"✅ به {count} نفر ارسال شد."})
                            del admin_states[user_id]
                            continue

                        if state['step'] == 'get_broadcast_text' and 'text' in msg:
                            target_cid = state['target']
                            if target_cid == 'all_groups':
                                success = 0
                                for cid in CHATS_INFO.keys():
                                    res = send_request("sendMessage", {"chat_id": cid, "text": msg['text']})
                                    if res.get("ok"): success += 1
                                send_request("sendMessage", {"chat_id": chat_id, "text": f"✅ به {success} گپ ارسال شد."})
                            else:
                                send_request("sendMessage", {"chat_id": target_cid, "text": msg['text']})
                                send_request("sendMessage", {"chat_id": chat_id, "text": "✅ به گپ ارسال شد."})
                            del admin_states[user_id]
                            continue

                    if "text" in msg:
                        text = msg["text"].strip()
                        if text in ['لینک', 'لینک ها'] and chat_id == CHAT_ID_SAMBAH_B:
                            if LINKS_LOCKED:
                                send_request("sendMessage", {"chat_id": chat_id, "text": "⛔️ **لینک‌ها توسط ادمین قفل شده‌اند.**"})
                            elif is_link_time_blocked():
                                send_request("sendMessage", {"chat_id": chat_id, "text": "⏰ دریافت لینک از ساعت ۲۳ الی ۱۰ ممنوع است."})
                            else:
                                send_request("sendMessage", {"chat_id": chat_id, "text": "🔗 **لیست لینک‌ها:**", "parse_mode": "Markdown", "reply_markup": get_links_keyboard()})
                        
                        if 'باطل کردن لینک' in text and chat_id == CHAT_ID_SAMBAH_B:
                            if not is_admin(chat_id, user_id): continue
                            send_request("sendMessage", {"chat_id": chat_id, "text": "⏳ در حال باطل کردن لینک‌ها..."})
                            report = "🔗 **گزارش:**\n\n"
                            for c_id, c_name in CHATS_INFO.items():
                                send_request("revokeChatInviteLink", {"chat_id": c_id, "invite_link": current_links[c_id]})
                                res_new = send_request("exportChatInviteLink", {"chat_id": c_id})
                                if res_new.get("ok"):
                                    new_link = res_new["result"]
                                    current_links[c_id] = new_link 
                                    report += f"✅ **{c_name}**\n{new_link}\n\n"
                                else:
                                    report += f"❌ **{c_name}**\nدلیل: {res_new.get('description')}\n\n"
                            send_request("sendMessage", {"chat_id": user_id, "text": report, "parse_mode": "Markdown"})
                            send_request("sendMessage", {"chat_id": chat_id, "text": "✅ **گزارش ارسال شد.**", "parse_mode": "Markdown"})

                if "callback_query" in update:
                    cq = update["callback_query"]
                    cq_id = cq["id"]
                    chat_id = str(cq["message"]["chat"]["id"])
                    user_id = str(cq["from"]["id"])
                    data = cq["data"]
                    message_id = cq["message"]["message_id"]
                    
                    send_request("answerCallbackQuery", {"callback_query_id": cq_id})
                    
                    if data == "unban_request":
                        for admin in BOT_ADMINS:
                            send_request("sendMessage", {"chat_id": admin, "text": f"📩 کاربر {user_id} درخواست لغو بن داده است."})
                        continue

                    if data.startswith("doz_"):
                        if chat_id not in games: continue
                        game = games[chat_id]
                        if not game['active']: continue
                        current_turn_player = game['p1'] if game['turn'] == '❌' else game['p2']
                        if user_id != current_turn_player: continue
                        idx = int(data.split("_")[1])
                        if game['board'][idx] != "": continue
                        player_symbol = game['turn']
                        game['board'][idx] = player_symbol
                        if check_winner(game['board'], player_symbol):
                            game['active'] = False
                            winner_name = game['p1_name'] if player_symbol == '❌' else game['p2_name']
                            send_request("editMessageText", {"chat_id": chat_id, "message_id": message_id, "text": f"🎉 **برنده:** {player_symbol} {winner_name}", "reply_markup": get_board_keyboard(game['board'])})
                            continue
                        if "" not in game['board']:
                            game['active'] = False
                            send_request("editMessageText", {"chat_id": chat_id, "message_id": message_id, "text": "🤝 **مساوی!**", "reply_markup": get_board_keyboard(game['board'])})
                            continue
                        game['turn'] = '⭕️' if player_symbol == '❌' else '❌'
                        next_player_name = game['p1_name'] if game['turn'] == '❌' else game['p2_name']
                        send_request("editMessageText", {"chat_id": chat_id, "message_id": message_id, "text": f"🎮 **دوز**\nنوبت: {game['turn']} {next_player_name}", "reply_markup": get_board_keyboard(game['board'])})
                        continue

                    if user_id not in BOT_ADMINS: continue
                    
                    if data == "admin_ban":
                        admin_states[user_id] = {'step': 'waiting_for_ban_id'}
                        send_request("sendMessage", {"chat_id": user_id, "text": "🚫 **آیدی عددی کاربر را برای بن کردن بفرستید:**"})
                        continue

                    if data == "admin_unban":
                        admin_states[user_id] = {'step': 'waiting_for_unban_id'}
                        send_request("sendMessage", {"chat_id": user_id, "text": "✅ **آیدی عددی کاربر را برای آنبن کردن بفرستید:**"})
                        continue

                    if data == "list_banned":
                        banned = load_banned_users()
                        if banned:
                            report = "🚫 **کاربران بن شده:**\n\n" + "\n".join([f"👤 آیدی: `{b_id}`" for b_id in banned])
                            send_request("sendMessage", {"chat_id": user_id, "text": report, "parse_mode": "Markdown"})
                        else:
                            send_request("sendMessage", {"chat_id": user_id, "text": "✅ هیچ کاربری بن نشده است."})
                        continue

                    if data == "find_owls":
                        if os.path.exists(USERS_DB_FILE):
                            with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                                users = json.load(f)
                            found_owls = []
                            for uid, uname in users.items():
                                if "𓅓" in uname or "🦉" in uname:
                                    found_owls.append(f"🦉 {uname} | `{uid}`")
                            if found_owls:
                                send_request("sendMessage", {"chat_id": user_id, "text": "🚨 **جغدها:**\n\n" + "\n".join(found_owls), "parse_mode": "Markdown"})
                            else:
                                send_request("sendMessage", {"chat_id": user_id, "text": "✅ جغدی یافت نشد."})
                        continue

                    if data == "lock_links":
                        LINKS_LOCKED = True
                        send_request("sendMessage", {"chat_id": user_id, "text": "🔒 لینک‌ها قفل شد."})
                    if data == "unlock_links":
                        LINKS_LOCKED = False
                        send_request("sendMessage", {"chat_id": user_id, "text": "🔓 لینک‌ها باز شد."})
                    
                    if data == "admin_broadcast":
                        admin_states[user_id] = {'step': 'choose_target'}
                        kb = json.dumps({"inline_keyboard": [[{"text": "پیوی همه", "callback_data": "target_pv"}],[{"text": "یک گپ", "callback_data": "target_group"}],[{"text": "همه گپ‌ها", "callback_data": "target_all"}]]}, ensure_ascii=False)
                        send_request("sendMessage", {"chat_id": user_id, "text": "🎯 کجا؟", "reply_markup": kb})
                    if data == "change_video":
                        admin_states[user_id] = {'step': 'waiting_for_video'}
                        send_request("sendMessage", {"chat_id": user_id, "text": "🎬 **فیلم جدید رو بفرست:**"})
                    if data == "target_pv":
                        admin_states[user_id] = {'step': 'get_text', 'target': 'pv'}
                        send_request("sendMessage", {"chat_id": user_id, "text": "📝 متن رو بفرست:"})
                    if data == "target_all":
                        admin_states[user_id] = {'step': 'get_broadcast_text', 'target': 'all_groups'}
                        send_request("sendMessage", {"chat_id": user_id, "text": "📝 متن رو بفرست:"})
                    if data == "target_group":
                        admin_states[user_id] = {'step': 'choose_group'}
                        kb = []
                        for cid, cname in CHATS_INFO.items():
                            kb.append([{"text": cname, "callback_data": f"broadcast_{cid}"}])
                        send_request("sendMessage", {"chat_id": user_id, "text": "🎯 کدوم گپ؟", "reply_markup": json.dumps({"inline_keyboard": kb}, ensure_ascii=False)})
                    if data.startswith("broadcast_"):
                        target_cid = data.split("_")[1]
                        admin_states[user_id] = {'step': 'get_broadcast_text', 'target': target_cid}
                        send_request("sendMessage", {"chat_id": user_id, "text": f"📝 متن رو بفرست:"})

                if "message" in update and "new_chat_members" in update["message"]:
                    msg = update["message"]
                    chat_id =

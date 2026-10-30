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

# 🎨 اسم‌های جدید (طبق فونت‌های ارسالی شما)
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
USERS_DB_FILE = 'users.txt'

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

# ⏰ تابع بررسی زمان (تغییر به ساعت 10 صبح)
def is_link_time_blocked():
    iran_tz = timezone(timedelta(hours=3, minutes=30))
    now = datetime.now(iran_tz)
    hour = now.hour
    # از ساعت ۲۳ شب تا ۱۰ صبح ممنوعه
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

def save_user(user_id):
    user_id = str(user_id)
    if os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, 'r') as f:
            users = f.read().splitlines()
        if user_id not in users:
            with open(USERS_DB_FILE, 'a') as f:
                f.write(f"{user_id}\n")
    else:
        with open(USERS_DB_FILE, 'w') as f:
            f.write(f"{user_id}\n")

def get_link(chat_id):
    res = send_request("exportChatInviteLink", {"chat_id": chat_id})
    if res.get("ok"):
        current_links[chat_id] = res["result"]
        return res["result"]
    return current_links.get(chat_id, "https://ble.ir/")

def get_welcome_keyboard():
    if is_link_time_blocked():
        return json.dumps({"inline_keyboard": []})
        
    # کیبورد خوش‌آمدگویی با اسم‌های جدید
    return json.dumps({
        "inline_keyboard": [
            [{"text": '𝐒𝐚𝐦𝐛𝐚𝐡 𝐆𝐓 (𝐁)💬', "url": get_link(CHAT_ID_SAMBAH_B)}],
            [{"text": '𓄂𝐒𝐚𝐦𝐛𝐚𝐡 𝐍𝐞𝐰𝐬🔔(𝐁)', "url": get_link(CHAT_ID_ETTELA_B)}],
            [{"text": '⚔️𝐒𝐚𝐦𝐛𝐚𝐡 𝐀𝐭𝐭𝐚𝐜𝐤𝐬⚔️', "url": get_link(CHAT_ID_HAMALAT)}],
            [{"text": '🎊𝐒𝐚𝐦𝐛𝐚𝐡 𝐆𝐚𝐦𝐞𝐬🎊', "url": get_link(CHAT_ID_DOORHAMI)}]
        ]
    }, ensure_ascii=False)

def get_links_keyboard():
    # منوی ۱۰ دکمه‌ای لاکچری
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
            [{"text": '➕ عضویت در کلن (۱)', "url": "https://ble.ir/SAMBAHY"}],
            [{"text": '➕ عضویت در کلن (۲)', "url": "https://ble.ir/mmdrza168"}]
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
                    
                    if not msg.get("from", {}).get("is_bot"):
                        save_user(user_id)
                    
                    if chat_id == user_id:
                        if user_id not in BOT_ADMINS:
                            if "text" in msg and msg["text"].strip() == '/start':
                                send_request("sendMessage", {
                                    "chat_id": chat_id, 
                                    "text": PV_WELCOME_TEXT, 
                                    "reply_markup": get_pv_keyboard()
                                })
                            continue 
                        
                        if "text" in msg and msg["text"].strip() in ['/start', 'پنل', '/panel']:
                            kb = json.dumps({
                                "inline_keyboard": [
                                    [{"text": "📢 ارسال پیام سراسری", "callback_data": "admin_broadcast"}],
                                    [{"text": "🎬 تغییر فیلم خوش‌آمدگویی", "callback_data": "change_video"}]
                                ]
                            }, ensure_ascii=False)
                            send_request("sendMessage", {"chat_id": chat_id, "text": "👑 **پنل مدیریت**\nخوش آمدید ادمین عزیز.", "reply_markup": kb, "parse_mode": "Markdown"})
                            continue

                    if user_id in admin_states:
                        state = admin_states[user_id]
                        
                        if state['step'] == 'waiting_for_video':
                            if "video" in msg:
                                with open(VIDEO_CACHE_FILE, 'w') as f:
                                    f.write(msg["video"]["file_id"])
                                saved_video_id = msg["video"]["file_id"]
                                send_request("sendMessage", {"chat_id": chat_id, "text": "✅ **فیلم خوش‌آمدگویی جدید ذخیره شد.**"})
                            else:
                                send_request("sendMessage", {"chat_id": chat_id, "text": "❌ لطفاً فقط یک **فیلم** (ویدیو) بفرستید."})
                            del admin_states[user_id]
                            continue

                        if "photo" in msg or "video" in msg:
                            if state['step'] in ['get_text', 'get_broadcast_text']:
                                send_request("sendMessage", {"chat_id": chat_id, "text": "❌ **خطا:** برای ارسال سراسری فقط می‌توانید متن بفرستید."})
                                continue
                        
                        if state['step'] == 'get_text' and state['target'] == 'pv' and 'text' in msg:
                            if os.path.exists(USERS_DB_FILE):
                                with open(USERS_DB_FILE, 'r') as f:
                                    all_users = f.read().splitlines()
                                count = 0
                                for uid in all_users:
                                    res = send_request("sendMessage", {"chat_id": uid, "text": f"📢 [پیام سراسری]\n\n{msg['text']}"})
                                    if res.get("ok"): count += 1
                                send_request("sendMessage", {"chat_id": chat_id, "text": f"✅ پیام به {count} کاربر ارسال شد."})
                            else:
                                send_request("sendMessage", {"chat_id": chat_id, "text": "❌ هنوز کاربری ربات رو استارت نکرده."})
                            del admin_states[user_id]
                            continue
                            
                        if state['step'] == 'get_broadcast_text' and 'text' in msg:
                            target_cid = state['target']
                            if target_cid == 'all_groups':
                                success = 0
                                for cid in CHATS_INFO.keys():
                                    res = send_request("sendMessage", {"chat_id": cid, "text": msg['text']})
                                    if res.get("ok"): success += 1
                                send_request("sendMessage", {"chat_id": chat_id, "text": f"✅ پیام به {success} گپ ارسال شد."})
                            else:
                                send_request("sendMessage", {"chat_id": target_cid, "text": msg['text']})
                                send_request("sendMessage", {"chat_id": chat_id, "text": "✅ پیام سراسری به گپ ارسال شد."})
                            del admin_states[user_id]
                            continue

                    if "text" in msg:
                        text = msg["text"].strip()
                        
                        if text in ['لینک', 'لینک ها'] and chat_id == CHAT_ID_SAMBAH_B:
                            if is_link_time_blocked():
                                send_request("sendMessage", {"chat_id": chat_id, "text": "⏰ دریافت لینک از ساعت ۲۳ الی ۱۰ ممنوع است."})
                            else:
                                send_request("sendMessage", {
                                    "chat_id": chat_id,
                                    "text": "🔗 **لیست لینک‌های گپ‌های سمباح:**",
                                    "parse_mode": "Markdown",
                                    "reply_markup": get_links_keyboard()
                                })
                            
                        if 'باطل کردن لینک' in text and chat_id == CHAT_ID_SAMBAH_B:
                            if not is_admin(chat_id, user_id): continue
                            
                            send_request("sendMessage", {"chat_id": chat_id, "text": "⏳ در حال باطل کردن لینک‌ها..."})
                            report = "🔗 **گزارش لینک‌ها:**\n\n"
                            for c_id, c_name in CHATS_INFO.items():
                                send_request("revokeChatInviteLink", {"chat_id": c_id, "invite_link": current_links[c_id]})
                                res_new = send_request("exportChatInviteLink", {"chat_id": c_id})
                                if res_new.get("ok"):
                                    new_link = res_new["result"]
                                    current_links[c_id] = new_link 
                                    report += f"✅ **{c_name}**\n{new_link}\n\n"
                                else:
                                    report += f"❌ **{c_name}**\nدلیل: {res_new.get('description', 'ربات ادمین نیست')}\n\n"
                            send_request("sendMessage", {"chat_id": user_id, "text": report, "parse_mode": "Markdown"})
                            send_request("sendMessage", {"chat_id": chat_id, "text": "✅ **لینک‌ها باطل شدند. گزارش به پیوی شما ارسال شد.**", "parse_mode": "Markdown"})

                if "callback_query" in update:
                    cq = update["callback_query"]
                    cq_id = cq["id"]
                    user_id = str(cq["from"]["id"])
                    data = cq["data"]
                    chat_id = str(cq["message"]["chat"]["id"])
                    
                    send_request("answerCallbackQuery", {"callback_query_id": cq_id})

                    if user_id not in BOT_ADMINS: continue

                    if data == "admin_broadcast":
                        admin_states[user_id] = {'step': 'choose_target'}
                        kb = json.dumps({
                            "inline_keyboard": [
                                [{"text": "ارسال به پیوی همه", "callback_data": "target_pv"}],
                                [{"text": "ارسال به یک گپ", "callback_data": "target_group"}],
                                [{"text": "ارسال به همه گپ‌ها", "callback_data": "target_all"}]
                            ]
                        }, ensure_ascii=False)
                        send_request("sendMessage", {"chat_id": user_id, "text": "🎯 کجا می‌خوای پیام سراسری بفرستی؟", "reply_markup": kb})

                    if data == "change_video":
                        admin_states[user_id] = {'step': 'waiting_for_video'}
                        send_request("sendMessage", {"chat_id": user_id, "text": "🎬 **لطفاً فیلم جدید خوش‌آمدگویی را بفرستید:**"})

                    if data == "target_pv":
                        admin_states[user_id] = {'step': 'get_text', 'target': 'pv'}
                        send_request("sendMessage", {"chat_id": user_id, "text": "📝 متن پیام سراسری رو بفرست (فقط متن):"})

                    if data == "target_all":
                        admin_states[user_id] = {'step': 'get_broadcast_text', 'target': 'all_groups'}
                        send_request("sendMessage", {"chat_id": user_id, "text": "📝 متن پیام رو بفرست تا به **همه گپ‌ها** ارسال بشه (فقط متن):"})

                    if data == "target_group":
                        admin_states[user_id] = {'step': 'choose_group'}
                        kb = []
                        for cid, cname in CHATS_INFO.items():
                            kb.append([{"text": cname, "callback_data": f"broadcast_{cid}"}])
                        send_request("sendMessage", {"chat_id": user_id, "text": "🎯 کدوم گپ؟", "reply_markup": json.dumps({"inline_keyboard": kb}, ensure_ascii=False)})

                    if data.startswith("broadcast_"):
                        target_cid = data.split("_")[1]
                        admin_states[user_id] = {'step': 'get_broadcast_text', 'target': target_cid}
                        send_request("sendMessage", {"chat_id": user_id, "text": f"📝 متن پیام رو بفرست تا به گپ {CHATS_INFO.get(target_cid, target_cid)} ارسال بشه (فقط متن):"})

                    continue

                if "message" in update and "new_chat_members" in update["message"]:
                    msg = update["message"]
                    chat_id = str(msg["chat"]["id"])
                    if chat_id == CHAT_ID_SAMBAH_B:
                        for member in msg["new_chat_members"]:
                            if member.get("is_bot"): continue
                            user_name = member.get("first_name", "دوست عزیز")
                            if saved_video_id:
                                send_video_to_target(saved_video_id, user_name)

        time.sleep(0.2)

    except KeyboardInterrupt:
        break
    except Exception as e:
        time.sleep(1)

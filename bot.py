import urllib.request
import json
import uuid
import time
import os

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

CHATS_INFO = {
    CHAT_ID_SAMBAH_B: "گپ سمباح (B)",
    CHAT_ID_ETTELA_B: "اطلاع رسانی سمباح (B)",
    CHAT_ID_SAMBAH_A: "گپ سمباح (A)",
    CHAT_ID_ETTELA_A: "اطلاع رسانی سمباح (A)",
    CHAT_ID_HAMALAT: "حملات سمباح",
    CHAT_ID_DOORHAMI: "دورهمی سمباح",
    CHAT_ID_VORUDI: "ورودی سمباح",
    CHAT_ID_AMIRALI: "پیام امیرعلی",
    CHAT_ID_MAJID: "پیام مجید",
    CHAT_ID_TITAP: "پیام تیتاپی ها"
}

ALLOWED_CHATS = list(CHATS_INFO.keys())

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

VIDEO_CACHE_FILE = 'video_id.txt'

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
    res = send_request("getChatMember", {"chat_id": chat_id, "user_id": user_id})
    if res.get("ok"):
        status = res["result"].get("status")
        if status in ["creator", "administrator"]:
            return True
    return False

def get_link(chat_id):
    res = send_request("exportChatInviteLink", {"chat_id": chat_id})
    if res.get("ok"):
        current_links[chat_id] = res["result"]
        return res["result"]
    return current_links.get(chat_id, "https://ble.ir/")

def get_welcome_keyboard():
    return json.dumps({
        "inline_keyboard": [
            [{"text": '💬 گپ سمباح (B)', "url": get_link(CHAT_ID_SAMBAH_B)}],
            [{"text": '🔔 اطلاع رسانی سمباح (B)', "url": get_link(CHAT_ID_ETTELA_B)}],
            [{"text": '🚀 حملات سمباح', "url": get_link(CHAT_ID_HAMALAT)}],
            [{"text": '🎊 دورهمی سمباح', "url": get_link(CHAT_ID_DOORHAMI)}]
        ]
    }, ensure_ascii=False)

def get_links_keyboard():
    return json.dumps({
        "inline_keyboard": [
            [{"text": '💬 گپ سمباح (B)', "url": get_link(CHAT_ID_SAMBAH_B)}],
            [{"text": '🔔 اطلاع رسانی سمباح (B)', "url": get_link(CHAT_ID_ETTELA_B)}],
            [{"text": '💬 گپ سمباح (A)', "url": get_link(CHAT_ID_SAMBAH_A)}],
            [{"text": '🔔 اطلاع رسانی سمباح (A)', "url": get_link(CHAT_ID_ETTELA_A)}],
            [{"text": '🚀 حملات سمباح', "url": get_link(CHAT_ID_HAMALAT)}],
            [{"text": '🎊 دورهمی سمباح', "url": get_link(CHAT_ID_DOORHAMI)}],
            [{"text": '🚷 ورودی سمباح', "url": get_link(CHAT_ID_VORUDI)}],
            [{"text": '🌚 پیام امیرعلی', "url": get_link(CHAT_ID_AMIRALI)}],
            [{"text": '🌚 پیام مجید', "url": get_link(CHAT_ID_MAJID)}],
            [{"text": '🌚 پیام تیتاپی ها', "url": get_link(CHAT_ID_TITAP)}]
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
    print("✅ فیلم از قبل ذخیره شده است.")

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
        updates = send_request("getUpdates", {"offset": last_update_id + 1, "timeout": 7}) # ⚡️ سرعت بالا رفت (۱۰ ثانیه)
        if updates.get("ok") and updates.get("result"):
            for update in updates["result"]:
                last_update_id = update["update_id"]
                if "message" in update:
                    msg = update["message"]
                    chat_id = str(msg["chat"]["id"])
                    
                    # 🚨 سیستم امنیتی: خروج از گپ غیرمجاز
                    if chat_id not in ALLOWED_CHATS:
                        print(f"⚠️ ربات به یک گپ غیرمجاز اضافه شد ({chat_id}). در حال خروج...")
                        send_request("leaveChat", {"chat_id": chat_id})
                        continue
                    
                    if "video" in msg and not msg.get("from", {}).get("is_bot"):
                        with open(VIDEO_CACHE_FILE, 'w') as f:
                            f.write(msg["video"]["file_id"])
                        saved_video_id = msg["video"]["file_id"]
                        print(f"\n✅ فیلم جدید ذخیره شد!")
                        
                    if "text" in msg:
                        text = msg["text"].strip()
                        user_id = str(msg["from"]["id"]) 
                        
                        # 🔐 بررسی ادمین بودن برای دستورات (فقط توی گپ سمباح B)
                        if text in ['لینک', 'لینک ها', '/del_links', 'باطل کردن لینک‌ها'] and chat_id == CHAT_ID_SAMBAH_B:
                            # اگه کاربر ادمین نبود، بیخیال شو
                            if not is_admin(chat_id, user_id):
                                continue 
                            
                            if text in ['لینک', 'لینک ها']:
                                send_request("sendMessage", {
                                    "chat_id": chat_id,
                                    "text": "🔗 **لیست لینک‌های گپ‌های سمباح:**",
                                    "parse_mode": "Markdown",
                                    "reply_markup": get_links_keyboard()
                                })
                                print("✅ منوی لینک‌ها ارسال شد.")
                                
                            elif text in ['/del_links', 'باطل کردن لینک‌ها']:
                                send_request("sendMessage", {"chat_id": chat_id, "text": "⏳ در حال باطل کردن لینک‌های قبلی و ساخت لینک‌های جدید..."})
                                
                                report = "🔗 **لینک‌های جدید گپ‌ها:**\n\n"
                                
                                for c_id, c_name in CHATS_INFO.items():
                                    res_revoke = send_request("revokeChatInviteLink", {"chat_id": c_id, "invite_link": current_links[c_id]})
                                    res_new = send_request("exportChatInviteLink", {"chat_id": c_id})
                                    
                                    if res_new.get("ok"):
                                        new_link = res_new["result"]
                                        current_links[c_id] = new_link 
                                        report += f"✅ **{c_name}**\n{new_link}\n\n"
                                    else:
                                        report += f"❌ **{c_name}** (خطا در ساخت لینک - ربات ادمین نیست؟)\n\n"
                                
                                send_request("sendMessage", {"chat_id": user_id, "text": report, "parse_mode": "Markdown"})
                                send_request("sendMessage", {"chat_id": chat_id, "text": "✅ **لینک‌های قبلی باطل شدند و لینک‌های جدید به پیوی شما ارسال شد.**", "parse_mode": "Markdown"})
                                print("✅ لینک‌ها باطل و جدید ساخته شدند.")

                    if "new_chat_members" in msg and chat_id == CHAT_ID_SAMBAH_B:
                        for member in msg["new_chat_members"]:
                            if member.get("is_bot"): continue
                            user_name = member.get("first_name", "دوست عزیز")
                            print(f"\n👋 کاربر جدید: {user_name}")
                            if saved_video_id:
                                print("⏳ ارسال خوش‌آمدگویی...")
                                result = send_video_to_target(saved_video_id, user_name)
                                print("🚀 ارسال شد!" if result.get("ok") else f"❌ خطا: {result}")

    except KeyboardInterrupt:
        break
    except Exception as e:
        time.sleep(1)

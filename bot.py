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
CHAT_ID_SAMBAH = '4884670320'
CHAT_ID_ETTELA = '5900955714'
CHAT_ID_HAMALAT = '5681028578'
CHAT_ID_DOORHAMI = '6023524639'

FALLBACK_LINK_SAMBAH = "https://ble.ir/join/4F2HQJ3rpD"
FALLBACK_LINK_ETTELA = "https://ble.ir/join/4zejnKnWu5"
FALLBACK_LINK_HAMALAT = "https://ble.ir/join/JA8nUskQGD"
FALLBACK_LINK_DOORHAMI = "https://ble.ir/join/8wN5aYsMf2"

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

def get_link(chat_id, fallback_link):
    res = send_request("exportChatInviteLink", {"chat_id": chat_id})
    return res["result"] if res.get("ok") else fallback_link

def get_keyboard():
    return json.dumps({
        "inline_keyboard": [
            [{"text": '💬گپ سمباح(B)', "url": get_link(CHAT_ID_SAMBAH, FALLBACK_LINK_SAMBAH)}],
            [{"text": '📢اطلاع رسانی سمباح(B)', "url": get_link(CHAT_ID_ETTELA, FALLBACK_LINK_ETTELA)}],
            [{"text": '⚔️حملات سمباح', "url": get_link(CHAT_ID_HAMALAT, FALLBACK_LINK_HAMALAT)}],
            [{"text": '🎉دورهمی سمباح(اجباری نیست)', "url": get_link(CHAT_ID_DOORHAMI, FALLBACK_LINK_DOORHAMI)}]
        ]
    }, ensure_ascii=False)

def send_video_to_target(video_file_id, user_name="دوست عزیز"):
    url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendVideo"
    boundary = uuid.uuid4().hex
    body = b''
    fields = {
        'chat_id': CHAT_ID_SAMBAH,
        'video': video_file_id,
        'caption': caption_template.format(name=user_name),
        'parse_mode': 'Markdown',
        'reply_markup': get_keyboard()
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

print("\n🤖 ربات روشن شد و روی سرور در حال اجراست...")

while True:
    try:
        updates = send_request("getUpdates", {"offset": last_update_id + 1, "timeout": 60})
        if updates.get("ok") and updates.get("result"):
            for update in updates["result"]:
                last_update_id = update["update_id"]
                if "message" in update:
                    msg = update["message"]
                    
                    # دریافت و ذخیره فیلم
                    if "video" in msg and not msg.get("from", {}).get("is_bot"):
                        with open(VIDEO_CACHE_FILE, 'w') as f:
                            f.write(msg["video"]["file_id"])
                        saved_video_id = msg["video"]["file_id"]
                        print(f"\n✅ فیلم جدید ذخیره شد!")
                        
                    # خوش آمدگویی
                    if "new_chat_members" in msg:
                        chat_id = str(msg["chat"]["id"])
                        if chat_id == CHAT_ID_SAMBAH:
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

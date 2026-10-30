import os

# 🔐 توکن
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DEFAULT_VIDEO_ID = "2065233217:421082582933511939:1:c68360172d75800342a475074d4a4b264b7d474003f6d08c1c6a2f3cfa2833b7"

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

BLOCKED_ROBOTS = ['940993529']
BOT_ADMINS = ['724704269', '566594483', '2065233217']

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

LINKS_LOCKED = False
admin_states = {}

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

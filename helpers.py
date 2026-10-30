import urllib.request
import json
import uuid
import os
from datetime import datetime, timezone, timedelta
from config import *

VIDEO_CACHE_FILE = 'welcome_video.txt'
USERS_DB_FILE = 'users_data.json'
BANNED_USERS_FILE = 'banned_users.json'

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

import time
import os
import json
from config import *
from helpers import *
from game import games, get_board_keyboard, check_winner

# 🔐 گرفتن آیدی خود ربات (برای سیستم خروج خودکار)
me = send_request("getMe")
BOT_ID = str(me["result"]["id"]) if me.get("ok") else ""

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
                    
                    # 🚪 سیستم خروج خودکار از گپ‌های غیرمجاز (به جز پیوی خود ربات)
                    if chat_id not in ALLOWED_CHATS and chat_id != str(msg["from"]["id"]):
                        print(f"⚠️ ربات به گپ غیرمجاز {chat_id} اضافه شد. در حال خروج...")
                        send_request("leaveChat", {"chat_id": chat_id})
                        continue 
                        
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
                    
                    # 🎮 شروع بازی دوز
                    if "text" in msg and msg["text"].strip() == 'دوز':
                        if "reply_to_message" in msg:
                            target_id = str(msg["reply_to_message"]["from"]["id"])
                            target_name = msg["reply_to_message"]["from"].get("first_name", "Player")
                            if target_id == user_id or target_id in BLOCKED_ROBOTS: continue
                            games[chat_id] = {'board': [""] * 16, 'turn': '❌', 'p1': user_id, 'p2': target_id, 'p1_name': user_name, 'p2_name': target_name, 'active': True}
                            send_request("sendMessage", {"chat_id": chat_id, "text": f"🎮 **بازی دوز شروع شد!**\n\n❌ {user_name}\n⭕️ {target_name}", "reply_markup": get_board_keyboard(games[chat_id]['board'])})
                            continue

                    # 💬 مدیریت پیوی (پنل ادمین)
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

                    # 🛠 پردازش وضعیت‌های ادمین
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
                                send_request("sendMessage", {"chat_id": chat_id, "text": f"✅ **فیلم خوش‌آمدگویی ذخیره شد.**\n\n🔑 **آیدی این فیلم:**\n`{msg['video']['file_id']}`\n\n_(این آیدی رو کپی کن و توی کد config.py، به عنوان DEFAULT_VIDEO_ID بذار تا با ریستارت سرور پاک نشه)_"})
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

                    # 🔗 دستورات متنی توی گپ‌ها
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

                # 🖱 پردازش کلیک روی دکمه‌های شیشه‌ای
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

                    # 🎮 پردازش دکمه‌های دوز
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

                # 🎉 خوش‌آمدگویی و سیستم خروج خودکار
                if "message" in update and "new_chat_members" in update["message"]:
                    msg = update["message"]
                    chat_id = str(msg["chat"]["id"])
                    
                    # 🚪 اگه ربات رو به گپ غیرمجاز اضافه کردن، خودش رو بیرون بندازه
                    if chat_id not in ALLOWED_CHATS:
                        send_request("leaveChat", {"chat_id": chat_id})
                        continue
                        
                    if chat_id == CHAT_ID_SAMBAH_B:
                        # 🔄 خوندن مجدد آیدی فیلم از فایل برای اطمینان
                        current_video_id = DEFAULT_VIDEO_ID
                        if os.path.exists(VIDEO_CACHE_FILE):
                            with open(VIDEO_CACHE_FILE, 'r') as f:
                                file_content = f.read().strip()
                                if file_content:
                                    current_video_id = file_content
                                    
                        for member in msg["new_chat_members"]:
                            if member.get("is_bot"): continue
                            user_name = member.get("first_name", "دوست عزیز")
                            if current_video_id and current_video_id != "YOUR_DEFAULT_VIDEO_ID_HERE":
                                send_video_to_target(current_video_id, user_name)

        time.sleep(0.2)

    except KeyboardInterrupt:
        break
    except Exception as e:
        time.sleep(1)

import os
import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Railway Variables required: BOT_TOKEN, ADMIN_ID
TOKEN = os.getenv('BOT_TOKEN', '').strip()
ADMIN_RAW = os.getenv('ADMIN_ID', '').strip()
if not TOKEN:
    raise RuntimeError('Set BOT_TOKEN in Railway Variables')
if not ADMIN_RAW.isdigit():
    raise RuntimeError('Set ADMIN_ID to your numeric Telegram user ID')
ADMIN_ID = int(ADMIN_RAW)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('course_bot')
bot = telebot.TeleBot(TOKEN)

# ===================== EDIT YOUR CONTENT HERE =====================
# Telegram photo file_id values can be obtained by sending each image to the bot
# and reading message.photo[-1].file_id, or use a public direct image URL.
AGE_IMAGE = 'https://i.ibb.co/Q7DBbpvZ/watermarked-img-5390942081179769641.png'
AGE_CAPTION = '𝘽𝙚𝙛𝙤𝙧𝙚 𝙘𝙤𝙣𝙩𝙞𝙣𝙪𝙞𝙣𝙜, 𝙥𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙛𝙞𝙧𝙢 𝙮𝙤𝙪 𝙖𝙧𝙚 18 𝙤𝙧 𝙤𝙡𝙙𝙚𝙧.'
DENIED_CAPTION = '𝘼𝙘𝙘𝙚𝙨𝙨 𝙙𝙚𝙣𝙞𝙚𝙙. 𝘽𝙤𝙩 𝙞𝙨 𝙤𝙣𝙡𝙮 𝙛𝙤𝙧 18+.'
WELCOME_IMAGE = 'https://imgh.in/host/03a6vy'
WELCOME_CAPTION = '''𝙒𝙚𝙡𝙘𝙤𝙢𝙚!
𝐇𝐄𝐑𝐄 𝐀𝐑𝐄 𝐏𝐋𝐀𝐍𝐒 ✅

🔥𝘽𝙃#𝘼𝙄 𝘽𝙀𝙃𝘼𝙉 
🔥𝘽𝙃𝘼𝘽𝙃𝙄 𝙑𝙄𝘿𝙀0𝙎 
🔥𝙈0𝙈 𝘼𝙉𝘿 𝙎𝙊#𝙉 
🔥𝙍!@𝙋𝙀 𝙑𝙄𝘿𝙀0𝙎 
🔥 𝙈𝘼𝙇#𝙇𝙐 𝙂𝙄𝙍𝙇 
🔥𝘽𝘼#𝙋 𝘽𝙀𝙏𝙄 
🔥𝙄𝙉𝘿𝙄𝘼𝙉 𝘾𝙃𝙄.#𝙇𝘿 
🔥𝙁𝙊𝙍𝙀𝙄𝙂𝙉 𝘾𝙃#.𝙄𝙇𝘿 
🔥𝘾𝘾𝙏𝙑 𝙊𝙔0 𝙍0𝙊𝙈 
🔥𝙅𝘼𝘽𝘼𝙍𝘿#𝙎𝙏𝙄 
🔥𝗢𝗨𝗧𝗗𝗢0𝗥 𝗩𝗜𝗗𝗘𝗢𝗦 
🔥𝗥@𝗡𝗗𝗜 𝗣𝗢#𝗥𝗡 
🔥𝗜𝗡𝗦𝗧𝗚𝗥𝗔𝗠 𝗠𝗠#𝗦 𝗔𝗟𝗟 
🔥𝗩𝗜𝗣 𝗣#𝗥𝗡 𝗛𝗨𝗕 𝗩𝗜𝗗𝗘𝗢𝗦 
🔥𝗔𝗟𝗟 𝗩𝗜𝗣 𝗠𝗘𝗚𝗔 𝗣𝗔𝗖𝗞 ( ₹169 ) 

𝘼𝙉𝙔 𝙋𝘼𝘾𝙆 𝘼𝙏 ₹49 ‼️

# Add/edit exactly 10 plan entries here. Leave unused entries with active=False.
PLANS = [
    {'id': 1, 'name': 'Plan 1', 'price': '199', 'validity': '30 days', 'videos': '50 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 2, 'name': 'Plan 2', 'price': '299', 'validity': '30 days', 'videos': '80 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 3, 'name': 'Plan 3', 'price': '399', 'validity': '60 days', 'videos': '100 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 4, 'name': 'Plan 4', 'price': '499', 'validity': '60 days', 'videos': '120 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 5, 'name': 'Plan 5', 'price': '599', 'validity': '90 days', 'videos': '150 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 6, 'name': 'Plan 6', 'price': '699', 'validity': '90 days', 'videos': '180 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 7, 'name': 'Plan 7', 'price': '799', 'validity': '120 days', 'videos': '200 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 8, 'name': 'Plan 8', 'price': '899', 'validity': '120 days', 'videos': '250 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 9, 'name': 'Plan 9', 'price': '999', 'validity': '180 days', 'videos': '300 videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
    {'id': 10, 'name': 'Plan 10', 'price': '1199', 'validity': '365 days', 'videos': 'All videos', 'image': '', 'qr': '', 'demo': 'https://example.com/demo', 'caption': '𝙇𝙚𝙖𝙧𝙣 𝙖𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 𝙥𝙖𝙘𝙚.', 'active': True},
]
# =================== END OF EDITABLE CONTENT =====================

# Telegram supports button styles only on some Bot API/client versions.
# We try the requested red/green/blue style sequence and gracefully fall back.
STYLE_SERIES = ['danger', 'success', 'primary', 'danger', 'success', 'primary', 'danger']
def button(text, data=None, url=None, style=None):
    kwargs = {'text': text}
    if data is not None: kwargs['callback_data'] = data
    if url is not None: kwargs['url'] = url
    if style:
        try: return InlineKeyboardButton(**kwargs, style=style)
        except (TypeError, ValueError): pass
    return InlineKeyboardButton(**kwargs)

def add_styled(kb, text, data=None, url=None, index=0):
    kb.add(button(text, data=data, url=url, style=STYLE_SERIES[index % len(STYLE_SERIES)]))

def get_plan(pid):
    return next((p for p in PLANS if p['id'] == pid and p.get('active')), None)

def send_photo_or_text(chat_id, image, caption, reply_markup=None):
    try:
        if image:
            bot.send_photo(chat_id, image, caption=caption, reply_markup=reply_markup)
        else:
            bot.send_message(chat_id, caption, reply_markup=reply_markup)
    except Exception:
        log.exception('Could not send configured image; sending text fallback')
        bot.send_message(chat_id, caption, reply_markup=reply_markup)

def send_age_gate(chat_id):
    kb = InlineKeyboardMarkup()
    kb.row(button('𝙔𝙚𝙨, 𝙄’𝙢 18+', 'age:yes', style='success'), button('𝙄’𝙢 𝙣𝙤𝙩', 'age:no', style='danger'))
    send_photo_or_text(chat_id, AGE_IMAGE, AGE_CAPTION, kb)

def send_home(chat_id):
    kb = InlineKeyboardMarkup()
    add_styled(kb, '𝙑𝙞𝙚𝙬 𝙥𝙡𝙖𝙣𝙨', 'plans', index=0)
    send_photo_or_text(chat_id, WELCOME_IMAGE, WELCOME_CAPTION, kb)

def send_plans(chat_id):
    kb = InlineKeyboardMarkup()
    for i, p in enumerate([p for p in PLANS if p.get('active')]):
        add_styled(kb, f"𝙋𝙡𝙖𝙣 {p['id']} · {p['name']} · ₹{p['price']}", f"plan:{p['id']}", index=i)
    add_styled(kb, '𝘽𝙖𝙘𝙠', 'home', index=len(PLANS))
    bot.send_message(chat_id, '𝘾𝙝𝙤𝙤𝙨𝙚 𝙖 𝙥𝙡𝙖𝙣:', reply_markup=kb)

def send_plan(chat_id, p):
    caption = (f"𝙋𝙡𝙖𝙣 : {p['name']}\n\n𝙋𝙧𝙞𝙘𝙚 - ₹{p['price']}\n𝙑𝙖𝙡𝙞𝙙𝙞𝙩𝙮 - {p['validity']}\n𝙑𝙞𝙙𝙚𝙤𝙨 - {p['videos']}\n\n{p['caption']}")
    kb = InlineKeyboardMarkup()
    add_styled(kb, '𝘽𝙪𝙮 𝙣𝙤𝙬', f"buy:{p['id']}", index=0)
    if p.get('demo') and p['demo'].startswith(('https://', 'http://')):
        add_styled(kb, '𝘿𝙚𝙢𝙤', url=p['demo'], index=1)
    add_styled(kb, '𝘾𝙝𝙖𝙣𝙜𝙚 𝙥𝙡𝙖𝙣', 'plans', index=2)
    send_photo_or_text(chat_id, p.get('image', ''), caption, kb)

def send_payment(chat_id, user_id, p):
    if not p.get('qr'):
        bot.send_message(chat_id, '𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙌𝙍 𝙞𝙨 𝙣𝙤𝙩 𝙨𝙚𝙩 𝙞𝙣 𝙘𝙤𝙙𝙚 𝙮𝙚𝙩.')
        return
    kb = InlineKeyboardMarkup()
    add_styled(kb, '𝙄 𝙥𝙖𝙞𝙙', f"paid:{p['id']}", index=0)
    add_styled(kb, '𝘽𝙖𝙘𝙠', f"plan:{p['id']}", index=1)
    caption = (f"𝙋𝙖𝙮 ₹{p['price']} using this QR.\n\n𝙎𝙩𝙚𝙥𝙨:\n1. 𝙎𝙘𝙖𝙣 𝙩𝙝𝙚 𝙌𝙍.\n2. 𝙋𝙖𝙮 𝙩𝙝𝙚 𝙚𝙭𝙖𝙘𝙩 𝙖𝙢𝙤𝙪𝙣𝙩.\n3. 𝙏𝙖𝙥 ‘𝙄 𝙥𝙖𝙞𝙙’.\n4. 𝙎𝙚𝙣𝙙 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩.\n𝙊𝙧𝙙𝙚𝙧 𝙧𝙚𝙛: {user_id}-{p['id']}")
    send_photo_or_text(chat_id, p['qr'], caption, kb)

# In-memory order state. Pending reviews are sent to ADMIN_ID; review is manual.
pending_screenshots = {}
user_waiting_screenshot = set()

@bot.message_handler(commands=['start'])
def start(message):
    user_waiting_screenshot.discard(message.from_user.id)
    send_age_gate(message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data in ('age:yes', 'age:no'))
def age_choice(call):
    bot.answer_callback_query(call.id)
    if call.data == 'age:no':
        kb = InlineKeyboardMarkup()
        add_styled(kb, '𝘽𝙖𝙘𝙠', 'age:back', index=0)
        bot.send_message(call.message.chat.id, DENIED_CAPTION, reply_markup=kb)
    else:
        # This is self-attestation only; it does not independently verify age.
        send_home(call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data == 'age:back')
def age_back(call):
    bot.answer_callback_query(call.id)
    send_age_gate(call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data == 'home')
def home(call):
    bot.answer_callback_query(call.id)
    send_home(call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data == 'plans')
def plans(call):
    bot.answer_callback_query(call.id)
    send_plans(call.message.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith('plan:'))
def plan_detail(call):
    bot.answer_callback_query(call.id)
    try: p = get_plan(int(call.data.split(':')[1]))
    except (ValueError, IndexError): p = None
    if p: send_plan(call.message.chat.id, p)

@bot.callback_query_handler(func=lambda c: c.data.startswith('buy:'))
def buy(call):
    bot.answer_callback_query(call.id)
    try: p = get_plan(int(call.data.split(':')[1]))
    except (ValueError, IndexError): p = None
    if p: send_payment(call.message.chat.id, call.from_user.id, p)

@bot.callback_query_handler(func=lambda c: c.data.startswith('paid:'))
def paid(call):
    bot.answer_callback_query(call.id)
    try: pid = int(call.data.split(':')[1]); p = get_plan(pid)
    except (ValueError, IndexError): p = None
    if not p: return
    user_waiting_screenshot.add(call.from_user.id)
    bot.send_message(call.message.chat.id, '𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙚𝙣𝙙 𝙩𝙝𝙚 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙖𝙨 𝙖 𝙥𝙝𝙤𝙩𝙤.')
    # Remember chosen plan while waiting for screenshot.
    pending_screenshots[call.from_user.id] = {'plan_id': pid, 'status': 'waiting'}

@bot.message_handler(content_types=['photo', 'text', 'document'])
def screenshot_handler(message):
    uid = message.from_user.id
    if uid not in user_waiting_screenshot:
        return
    if message.content_type != 'photo':
        bot.reply_to(message, '𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙖𝙨 𝙖 𝙥𝙝𝙤𝙩𝙤.')
        return
    state = pending_screenshots.get(uid, {})
    pid = state.get('plan_id')
    p = get_plan(pid) if pid else None
    if not p:
        bot.reply_to(message, '𝙋𝙡𝙖𝙣 𝙞𝙣𝙛𝙤 𝙢𝙞𝙨𝙨𝙞𝙣𝙜. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙩𝙧𝙮 𝙖𝙜𝙖𝙞𝙣.')
        return
    user_waiting_screenshot.discard(uid)
    file_id = message.photo[-1].file_id
    kb = InlineKeyboardMarkup()
    add_styled(kb, '𝘼𝙥𝙥𝙧𝙤𝙫𝙚', f'review:approve:{uid}:{pid}', index=1)
    add_styled(kb, '𝙍𝙚𝙟𝙚𝙘𝙩', f'review:reject:{uid}:{pid}', index=0)
    try:
        bot.send_photo(ADMIN_ID, file_id,
            caption=(f"𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩\n𝙐𝙨𝙚𝙧 𝙄𝘿: {uid}\n𝙋𝙡𝙖𝙣: {p['name']}\n𝘼𝙢𝙤𝙪𝙣𝙩: ₹{p['price']}"), reply_markup=kb)
        bot.reply_to(message, '𝙎𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙨𝙪𝙗𝙢𝙞𝙩𝙩𝙚𝙙.')
    except Exception:
        log.exception('Failed sending screenshot to admin')
        user_waiting_screenshot.add(uid)
        bot.reply_to(message, '𝙎𝙪𝙗𝙢𝙞𝙨𝙨𝙞𝙤𝙣 𝙛𝙖𝙞𝙡𝙚𝙙. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙩𝙧𝙮 𝙖𝙜𝙖𝙞𝙣.')

@bot.callback_query_handler(func=lambda c: c.data.startswith('review:'))
def review(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, 'Not allowed', show_alert=True)
        return
    parts = call.data.split(':')
    if len(parts) != 4 or parts[1] not in ('approve', 'reject'):
        bot.answer_callback_query(call.id, 'Invalid action', show_alert=True)
        return
    action, uid_s, pid_s = parts[1], parts[2], parts[3]
    try: uid, pid = int(uid_s), int(pid_s)
    except ValueError:
        bot.answer_callback_query(call.id, 'Invalid order', show_alert=True); return
    p = get_plan(pid)
    status = 'approved' if action == 'approve' else 'rejected'
    try:
        bot.send_message(uid, '𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙙. 𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪.' if action == 'approve' else '𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙧𝙚𝙟𝙚𝙘𝙩𝙚𝙙. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙖𝙙𝙢𝙞𝙣 𝙞𝙛 𝙮𝙤𝙪 𝙩𝙝𝙞𝙣𝙠 𝙩𝙝𝙞𝙨 𝙞𝙨 𝙖 𝙢𝙞𝙨𝙩𝙖𝙠𝙚.')
    except Exception:
        log.exception('Could not notify user %s', uid)
    bot.answer_callback_query(call.id, status.title())
    try: bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    except Exception: pass
    bot.send_message(ADMIN_ID, f'𝙊𝙧𝙙𝙚𝙧 {status}: user {uid}, plan {p["name"] if p else pid}.')

if __name__ == '__main__':
    log.info('Starting fixed-config bot (no admin panel)')
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
    kb.add(btn("⬅ Back to plan", f"u:plan:{pid}"))
    bot.send_photo(call.message.chat.id, p["qr_id"],
                   caption=p["qr_caption"] or f"Pay ₹{p['price']} using this QR. Order #{oid}",
                   caption_entities=entities_from_json(p["qr_entities"]) or None,
                   reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("u:submit:"))
def user_submit(call):
    bot.answer_callback_query(call.id)
    try:
        oid = int(call.data.rsplit(":", 1)[1])
    except ValueError:
        return
    with db() as con:
        row = con.execute("SELECT id FROM orders WHERE id=? AND user_id=? AND status='awaiting_payment'",
                          (oid, call.from_user.id)).fetchone()
    if not row:
        bot.send_message(call.message.chat.id, "Order not found or already submitted.")
        return
    states[call.from_user.id] = {"state": "payment_screenshot", "order_id": oid}
    bot.send_message(call.message.chat.id, "Payment screenshot ko PHOTO ke roop mein bhejo. Admin payment manually verify karega.")


@bot.callback_query_handler(func=lambda c: c.data == "a:home")
def admin_home_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    states.pop(call.from_user.id, None)
    send_admin(call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "a:cancel")
def admin_cancel_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    states.pop(call.from_user.id, None)
    send_admin(call.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == "a:add")
def add_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    states[call.from_user.id] = {"state": "add_name", "data": {}}
    bot.send_message(call.message.chat.id, "➕ Add plan: plan name bhejo.")


@bot.callback_query_handler(func=lambda c: c.data == "a:edit")
def edit_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb, rows = list_plan_keyboard("editpick", False)
    bot.send_message(call.message.chat.id, "Choose a plan to edit:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "a:remove")
def remove_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb, rows = list_plan_keyboard("removepick", True)
    bot.send_message(call.message.chat.id, "Choose plan to deactivate:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "a:list")
def list_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    with db() as con:
        rows = con.execute("SELECT id,name,price,active FROM plans ORDER BY id DESC LIMIT 80").fetchall()
    if not rows:
        bot.send_message(call.message.chat.id, "No plans yet. Tap Add plan.")
    for p in rows:
        bot.send_message(call.message.chat.id, f"#{p['id']} {p['name']} — ₹{p['price']} — {'active' if p['active'] else 'inactive'}")


@bot.callback_query_handler(func=lambda c: c.data == "a:welcome")
def welcome_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb = InlineKeyboardMarkup()
    kb.add(btn("Set welcome caption + emoji", "a:welcometext"))
    kb.add(btn("Set welcome image", "a:welcomeimage"))
    kb.add(btn("Clear welcome image", "a:clearwelcome"))
    kb.add(btn("⬅ Admin menu", "a:home"))
    bot.send_message(call.message.chat.id, "Welcome settings:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "a:welcometext")
def welcome_text_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    prompt(call.message.chat.id, call.from_user.id, "welcome_text",
           "Send the full welcome text with Premium custom emoji(s). The bot saves custom emoji IDs automatically.")


@bot.callback_query_handler(func=lambda c: c.data == "a:welcomeimage")
def welcome_image_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    prompt(call.message.chat.id, call.from_user.id, "welcome_image", "Welcome image PHOTO bhejo.")


@bot.callback_query_handler(func=lambda c: c.data == "a:clearwelcome")
def clear_welcome_cb(call):
    if not admin_callback(call):
        return
    set_setting("welcome_image", "")
    bot.answer_callback_query(call.id, "Cleared")
    bot.send_message(call.message.chat.id, "Welcome image cleared.")


@bot.callback_query_handler(func=lambda c: c.data == "a:demo")
def demo_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    kb = InlineKeyboardMarkup()
    kb.add(btn("Set/change link", "a:setdemo"))
    kb.add(btn("Clear link", "a:cleardemo"))
    kb.add(btn("⬅ Admin menu", "a:home"))
    bot.send_message(call.message.chat.id, "Demo link settings:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == "a:setdemo")
def setdemo_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    prompt(call.message.chat.id, call.from_user.id, "demo_link", "Full demo URL bhejo (https://t.me/...).")


@bot.callback_query_handler(func=lambda c: c.data == "a:cleardemo")
def cleardemo_cb(call):
    if not admin_callback(call):
        return
    set_setting("demo_link", "")
    bot.answer_callback_query(call.id, "Cleared")
    bot.send_message(call.message.chat.id, "Demo link cleared.")


@bot.callback_query_handler(func=lambda c: c.data == "a:emoji")
def emoji_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    prompt(call.message.chat.id, call.from_user.id, "button_emoji",
           "Ab ek message bhejo jisme custom Premium emoji ho. Bot us message ki pehli custom emoji ID save karega aur future supported button icons mein use karega.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("a:editpick:"))
def editpick_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    try:
        pid = int(call.data.rsplit(":", 1)[1])
    except ValueError:
        return
    p = get_plan(pid)
    if not p:
        bot.send_message(call.message.chat.id, "Plan not found.")
        return
    kb = InlineKeyboardMarkup()
    for label, field in [
        ("Name", "name"), ("Price", "price"), ("Description + custom emoji", "description"),
        ("Plan image", "image"), ("Payment QR", "qr"), ("QR caption + emoji", "qrcaption"),
        ("Activate/deactivate", "active")]:
        kb.add(btn(label, f"a:field:{pid}:{field}"))
    kb.add(btn("⬅ Admin menu", "a:home"))
    bot.send_message(call.message.chat.id, f"Editing #{pid} {p['name']}. Choose field:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("a:removepick:"))
def removepick_cb(call):
    if not admin_callback(call):
        return
    try:
        pid = int(call.data.rsplit(":", 1)[1])
    except ValueError:
        bot.answer_callback_query(call.id, "Invalid plan.")
        return
    with db() as con:
        con.execute("UPDATE plans SET active=0 WHERE id=?", (pid,))
    bot.answer_callback_query(call.id, "Plan deactivated")
    bot.send_message(call.message.chat.id, f"Plan #{pid} deactivated; old orders preserved.")


@bot.callback_query_handler(func=lambda c: c.data.startswith("a:field:"))
def field_cb(call):
    if not admin_callback(call):
        return
    parts = call.data.split(":")
    if len(parts) != 4:
        bot.answer_callback_query(call.id, "Invalid field.")
        return
    try:
        pid = int(parts[2])
    except ValueError:
        bot.answer_callback_query(call.id, "Invalid plan.")
        return
    field = parts[3]
    map_fields = {
        "name": ("edit_name", "New plan name bhejo."),
        "price": ("edit_price", "New price bhejo, e.g. 199."),
        "description": ("edit_description", "New caption/description custom emoji ke saath bhejo."),
        "image": ("edit_image", "New plan image PHOTO bhejo."),
        "qr": ("edit_qr", "New payment QR PHOTO bhejo."),
        "qrcaption": ("edit_qrcaption", "New QR caption custom emoji ke saath bhejo."),
        "active": ("edit_active", "Send 1 to activate or 0 to deactivate.")
    }
    if field not in map_fields:
        bot.answer_callback_query(call.id, "Invalid field.")
        return
    bot.answer_callback_query(call.id)
    st, text = map_fields[field]
    prompt(call.message.chat.id, call.from_user.id, st, text, plan_id=pid)


@bot.callback_query_handler(func=lambda c: c.data == "a:pending")
def pending_cb(call):
    if not admin_callback(call):
        return
    bot.answer_callback_query(call.id)
    with db() as con:
        rows = con.execute("SELECT id FROM orders WHERE status='pending' ORDER BY id DESC LIMIT 30").fetchall()
    if not rows:
        bot.send_message(call.message.chat.id, "No pending payments.")
    for r in rows:
        send_order_admin(call.message.chat.id, r["id"])


def send_order_admin(chat_id, oid):
    with db() as con:
        o = con.execute("""SELECT o.*,p.name,p.price FROM orders o LEFT JOIN plans p ON p.id=o.plan_id WHERE o.id=?""", (oid,)).fetchone()
    if not o:
        return
    caption = f"Order #{oid}\nUser ID: {o['user_id']}\nPlan: {o['name'] or 'Unavailable'}\nAmount: ₹{o['price'] or '?'}\nStatus: {o['status']}"
    kb = InlineKeyboardMarkup()
    if o["status"] == "pending":
        kb.row(btn("✅ Approve", f"a:approve:{oid}", style="success"),
               btn("❌ Reject", f"a:reject:{oid}", style="danger"))
    if o["screenshot_id"]:
        bot.send_photo(chat_id, o["screenshot_id"], caption=caption, reply_markup=kb if o["status"] == "pending" else None)
    else:
        bot.send_message(chat_id, caption, reply_markup=kb if o["status"] == "pending" else None)


@bot.callback_query_handler(func=lambda c: c.data.startswith("a:approve:") or c.data.startswith("a:reject:"))
def review_cb(call):
    if not admin_callback(call):
        return
    parts = call.data.split(":")
    action = parts[1]
    try:
        oid = int(parts[2])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Invalid order.")
        return
    status = "approved" if action == "approve" else "rejected"
    with db() as con:
        o = con.execute("SELECT user_id,status FROM orders WHERE id=?", (oid,)).fetchone()
        if not o or o["status"] != "pending":
            bot.answer_callback_query(call.id, "Already reviewed or missing.", show_alert=True)
            return
        con.execute("UPDATE orders SET status=? WHERE id=?", (status, oid))
    bot.answer_callback_query(call.id, "Saved")
    try:
        bot.send_message(o["user_id"], "✅ Payment approved!" if status == "approved" else "❌ Payment rejected. Contact admin if you think this is a mistake.")
    except Exception:
        log.exception("Could not notify user")
    bot.send_message(call.message.chat.id, f"Order #{oid} marked {status}.")


def capture_custom_entities(message):
    return entity_data(getattr(message, "entities", None))


@bot.message_handler(content_types=["text", "photo"])
def form_handler(message):
    uid = message.from_user.id
    info = states.get(uid)
    if not info:
        return
    state = info["state"]
    if message.content_type == "text" and message.text and message.text.strip().lower() == "/cancel":
        states.pop(uid, None)
        bot.reply_to(message, "Cancelled.")
        if is_admin(uid):
            send_admin(message.chat.id)
        return

    if state == "payment_screenshot":
        if message.content_type != "photo":
            bot.reply_to(message, "Screenshot ko PHOTO ke roop mein bhejo.")
            return
        oid = info["order_id"]
        file_id = message.photo[-1].file_id
        with db() as con:
            cur = con.execute("""UPDATE orders SET screenshot_id=?,status='pending'
                WHERE id=? AND user_id=? AND status='awaiting_payment'""", (file_id, oid, uid))
            order = con.execute("SELECT id FROM orders WHERE id=?", (oid,)).fetchone()
            changed = cur.rowcount
        states.pop(uid, None)
        if not changed:
            bot.reply_to(message, "Order is no longer awaiting a screenshot.")
            return
        bot.reply_to(message, "Screenshot received. Admin will verify payment manually.")
        try:
            send_order_admin(ADMIN_ID, oid)
        except Exception:
            log.exception("Could not notify admin about order")
        return

    if not is_admin(uid):
        states.pop(uid, None)
        return

    if state in ("welcome_text", "edit_description", "edit_qrcaption"):
        if message.content_type != "text":
            bot.reply_to(message, "Text message bhejo, custom emoji ke saath.")
            return
        text = message.text
        ents = capture_custom_entities(message)
        if state == "welcome_text":
            set_setting("welcome_caption", text)
            set_setting("welcome_entities", json.dumps(ents))
            states.pop(uid, None)
            bot.reply_to(message, f"✅ Welcome text saved. Custom emoji entities found: {len(ents)}")
            return
        pid = info["plan_id"]
        with db() as con:
            if state == "edit_description":
                con.execute("UPDATE plans SET description=?,description_entities=? WHERE id=?",
                            (text, json.dumps(ents), pid))
            else:
                con.execute("UPDATE plans SET qr_caption=?,qr_entities=? WHERE id=?",
                            (text, json.dumps(ents), pid))
        states.pop(uid, None)
        bot.reply_to(message, f"✅ Saved. Custom emoji entities found: {len(ents)}")
        return

    if state == "button_emoji":
        ents = capture_custom_entities(message)
        if not ents:
            bot.reply_to(message, "Is message mein custom_emoji entity nahi mili. Telegram Premium custom emoji ko direct message mein insert karke bhejo; plain emoji se ID nahi milti.")
            return
        set_setting("button_emoji_id", ents[0]["custom_emoji_id"])
        states.pop(uid, None)
        bot.reply_to(message, "✅ Custom emoji ID saved for supported button icons.")
        return

    if state == "welcome_image":
        if message.content_type != "photo":
            bot.reply_to(message, "Welcome image PHOTO bhejo.")
            return
        set_setting("welcome_image", message.photo[-1].file_id)
        states.pop(uid, None)
        bot.reply_to(message, "✅ Welcome image saved.")
        return

    if state == "demo_link":
        if message.content_type != "text" or not valid_url(message.text.strip()):
            bot.reply_to(message, "Full valid URL bhejo, e.g. https://t.me/yourchannel")
            return
        set_setting("demo_link", message.text.strip())
        states.pop(uid, None)
        bot.reply_to(message, "✅ Demo link saved.")
        return

    if state.startswith("add_"):
        data = info.setdefault("data", {})
        if state == "add_name":
            if message.content_type != "text" or not message.text.strip():
                bot.reply_to(message, "Plan name text mein bhejo.")
                return
            data["name"] = message.text.strip()[:100]
            info["state"] = "add_price"
            bot.send_message(message.chat.id, "Price bhejo (e.g. 199).")
        elif state == "add_price":
            if message.content_type != "text" or not re.fullmatch(r"\d{1,9}(?:\.\d{1,2})?", message.text.strip()):
                bot.reply_to(message, "Valid price bhejo, e.g. 199 or 199.50.")
                return
            data["price"] = message.text.strip()
            info["state"] = "add_description"
            bot.send_message(message.chat.id, "Plan caption custom emoji ke saath bhejo, ya /skip.")
        elif state == "add_description":
            if message.content_type != "text":
                bot.reply_to(message, "Caption text mein bhejo.")
                return
            if message.text.strip() == "/skip":
                data["description"], data["description_entities"] = "", "[]"
            else:
                data["description"] = message.text[:3500]
                data["description_entities"] = json.dumps(capture_custom_entities(message))
            info["state"] = "add_image"
            bot.send_message(message.chat.id, "Plan image PHOTO bhejo, ya /skip.")
        elif state == "add_image":
            if message.content_type == "photo":
                data["image_id"] = message.photo[-1].file_id
            elif message.content_type == "text" and message.text.strip() == "/skip":
                data["image_id"] = ""
            else:
                bot.reply_to(message, "Photo bhejo ya /skip.")
                return
            info["state"] = "add_qr"
            bot.send_message(message.chat.id, "Payment QR PHOTO bhejo (required).")
        elif state == "add_qr":
            if message.content_type != "photo":
                bot.reply_to(message, "Payment QR ko PHOTO ke roop mein bhejo.")
                return
            data["qr_id"] = message.photo[-1].file_id
            info["state"] = "add_qrcaption"
            bot.send_message(message.chat.id, "QR caption custom emoji ke saath bhejo, ya /skip.")
        elif state == "add_qrcaption":
            if message.content_type != "text":
                bot.reply_to(message, "QR caption text mein bhejo.")
                return
            if message.text.strip() == "/skip":
                data["qr_caption"], data["qr_entities"] = "", "[]"
            else:
                data["qr_caption"] = message.text[:1000]
                data["qr_entities"] = json.dumps(capture_custom_entities(message))
            with db() as con:
                cur = con.execute("""INSERT INTO plans
                    (name,price,description,description_entities,image_id,qr_id,qr_caption,qr_entities,active)
                    VALUES(?,?,?,?,?,?,?,?,1)""",
                    (data["name"], data["price"], data.get("description", ""),
                     data.get("description_entities", "[]"), data.get("image_id", ""),
                     data["qr_id"], data.get("qr_caption", ""), data.get("qr_entities", "[]")))
                pid = cur.lastrowid
            states.pop(uid, None)
            bot.send_message(message.chat.id, f"✅ Plan #{pid} created and saved.")
            send_admin(message.chat.id)
        return

    if state.startswith("edit_"):
        pid = info["plan_id"]
        field_map = {
            "edit_name": ("name", "text"),
            "edit_price": ("price", "text"),
            "edit_description": ("description", "text"),
            "edit_image": ("image_id", "photo"),
            "edit_qr": ("qr_id", "photo"),
            "edit_qrcaption": ("qr_caption", "text"),
            "edit_active": ("active", "text")
        }
        if state not in field_map:
            return
        field, expected = field_map[state]
        if expected == "photo":
            if message.content_type != "photo":
                bot.reply_to(message, "Is field ke liye PHOTO bhejo.")
                return
            value = message.photo[-1].file_id
        else:
            if message.content_type != "text":
                bot.reply_to(message, "Text bhejo.")
                return
            value = message.text.strip()
            if field == "price" and not re.fullmatch(r"\d{1,9}(?:\.\d{1,2})?", value):
                bot.reply_to(message, "Valid price bhejo, e.g. 199.")
                return
            if field == "active" and value not in ("0", "1"):
                bot.reply_to(message, "1 = active, 0 = inactive.")
                return
            if field == "name" and not value:
                bot.reply_to(message, "Name cannot be empty.")
                return
        with db() as con:
            if field == "description":
                con.execute("UPDATE plans SET description=?,description_entities=? WHERE id=?",
                            (value, json.dumps(capture_custom_entities(message)), pid))
            elif field == "qr_caption":
                con.execute("UPDATE plans SET qr_caption=?,qr_entities=? WHERE id=?",
                            (value, json.dumps(capture_custom_entities(message)), pid))
            else:
                if field == "active":
                    value = int(value)
                con.execute(f"UPDATE plans SET {field}=? WHERE id=?", (value, pid))
        states.pop(uid, None)
        bot.reply_to(message, f"✅ Plan #{pid} updated and saved.")
        p = get_plan(pid)
        if p:
            kb = InlineKeyboardMarkup()
            for label, f in [("Name","name"),("Price","price"),("Description + emoji","description"),
                             ("Plan image","image"),("Payment QR","qr"),("QR caption + emoji","qrcaption"),
                             ("Activate/deactivate","active")]:
                kb.add(btn(label, f"a:field:{pid}:{f}"))
            kb.add(btn("⬅ Admin menu", "a:home"))
            bot.send_message(message.chat.id, f"Editing #{pid} {p['name']}. Choose another field:", reply_markup=kb)
        return


if __name__ == "__main__":
    setup_db()
    log.info("Starting bot with database %s", DB_PATH)
    # Important: only ONE running instance may poll this token.
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=25)

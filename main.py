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
AGE_IMAGE = ''
AGE_CAPTION = '𝘽𝙚𝙛𝙤𝙧𝙚 𝙘𝙤𝙣𝙩𝙞𝙣𝙪𝙞𝙣𝙜, 𝙥𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙛𝙞𝙧𝙢 𝙮𝙤𝙪 𝙖𝙧𝙚 18 𝙤𝙧 𝙤𝙡𝙙𝙚𝙧.'
DENIED_CAPTION = '𝘼𝙘𝙘𝙚𝙨𝙨 𝙙𝙚𝙣𝙞𝙚𝙙. 𝘽𝙤𝙩 𝙞𝙨 𝙤𝙣𝙡𝙮 𝙛𝙤𝙧 18+.'
WELCOME_IMAGE = ''
WELCOME_CAPTION = '''🌟 𝐅𝐔𝐋𝐋 𝐏𝐗𝟒𝐍 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍 🌟

🔥 𝐌𝐎𝐌 𝐀𝐍𝐃 𝐒𝟎𝐍
🔥 𝐒𝐈𝐒 𝐀𝐍𝐃 𝐁𝐑𝟎
🔥 𝐃𝐄𝐒𝐈 / 𝐅𝐎𝐑𝐄𝐈𝐆𝐍 𝐂𝐱𝐏 
🔥 𝐂𝐗𝐏 𝐊𝐈𝐃𝐒
🔥 𝐅𝟎𝐑𝐂𝐄𝐃 𝐒₹𝐗 
🔥 𝐇@𝐑𝐃 𝐂𝟎𝐑𝐄 
🔥 𝐑𝐀𝐗𝐏𝐄 𝐕𝐈𝐃𝐄𝐎𝐒
🔥 𝐂𝐎𝐔𝐏𝐋₹ 𝐌𝐌$

!! 𝙉𝙀𝙒 𝘼𝘿𝘿𝙀𝘿 !! 
🔥55𝙆 𝘼𝙇𝙇 𝙄𝙉𝙎𝙏𝘼 𝙇𝙀𝘼𝙆𝙎 😍
🔥𝘼𝙇𝙇 𝙈𝙈𝙎 👀

☠️ 𝐀𝐋𝐋 𝐅𝐎𝐑 49 𝐑𝐒 ☠️

𝙄𝙁 𝙔𝙊𝙐 𝙒𝘼𝙉𝙏 𝘾𝙇𝙄𝘾𝙆 𝙊𝙉 𝙄 𝙒𝘼𝙉𝙏 ✅

𝙋𝙍𝙄𝘾𝙀 𝙄𝙎 𝙅𝙐𝙎𝙏 49 ₹ ☠️.'''

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
    # Send welcome text first, then show every active plan immediately.
    send_photo_or_text(chat_id, WELCOME_IMAGE, WELCOME_CAPTION)
    send_plans_direct(chat_id)

def send_plans_direct(chat_id):
    for p in [p for p in PLANS if p.get('active')]:
        send_plan(chat_id, p)

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

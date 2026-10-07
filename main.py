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
AGE_IMAGE = 'https://ibb.co/5ghpxM6Z'
AGE_CAPTION = '𝘽𝙚𝙛𝙤𝙧𝙚 𝙘𝙤𝙣𝙩𝙞𝙣𝙪𝙞𝙣𝙜, 𝙥𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙛𝙞𝙧𝙢 𝙮𝙤𝙪 𝙖𝙧𝙚 18 𝙤𝙧 𝙤𝙡𝙙𝙚𝙧.'
DENIED_CAPTION = '𝘼𝙘𝙘𝙚𝙨𝙨 𝙙𝙚𝙣𝙞𝙚𝙙. 𝘽𝙤𝙩 𝙞𝙨 𝙤𝙣𝙡𝙮 𝙛𝙤𝙧 18+.'
WELCOME_IMAGE = 'https://myimgs.org/storage/images/48905/1000200263.jpg'
WELCOME_CAPTION = '''𝙃𝙀𝙔 👋🏻, 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙤𝙪𝙧 𝙫𝙞𝙥 𝙗𝙤𝙩 😍
𝙏𝙃𝙄𝙎 𝘽𝙊𝙏 𝘾𝙊𝙉𝘼𝙏𝘼𝙄𝙉 𝙁𝙊𝙇𝙇𝙊𝙒𝙄𝙉𝙂 𝙋𝙇𝘼𝙉𝙎 ✅ 
𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 𝙋𝙍𝙄𝘾𝙀 𝙄𝙎 𝙅𝙐𝙎𝙏 ₹39 ‼️

| 🔥𝘾𝙃𝙄!𝙇𝘿 𝙑𝙄𝘿𝙀𝙊𝙎 ( 𝘾𝙋 ) ( 𝘾𝙃𝙊𝙏𝙀 𝘽𝘼𝘾𝘾𝙃𝙀 ) 
| 🔥𝘽𝙃𝘼𝘽𝙃𝙄 𝙑𝙄𝘿𝙀0𝙎 
| 🔥𝙈0𝙈 𝘼𝙉𝘿 𝙎𝙊#𝙉 
| 🔥𝙍!@𝙋𝙀 𝙑𝙄𝘿𝙀0𝙎
| 🔥𝘽𝘼#𝙋 𝘽𝙀𝙏𝙄 
| 🔥𝗜𝗡𝗦𝗧𝗚𝗥𝗔𝗠 𝗠𝗠#𝗦 𝗔𝗟𝗟 
| 🔥𝙂𝙄𝙍𝙇𝙎 𝙒𝙄𝙏𝙃 𝘼𝙉𝙄𝙈!𝘼𝙇 
| 🔥 𝙈𝙄𝙓 𝙂𝙍𝙊𝙐𝙋 70𝙆 𝙑𝙄𝘿𝙀𝙊 
| 🔥𝘽𝙃𝘼𝙄 𝘽𝙀𝙃𝘼𝙉
| 🔥𝗔𝗟𝗟 𝗩𝗜𝗣 𝗠𝗘𝗚𝗔 𝗣𝗔𝗖𝗞 

𝘽𝙀𝙉𝙄𝙁𝙄𝙏𝙎 𝙊𝙁 𝙊𝙐𝙍 𝘽𝙊𝙏 ✅
1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙑𝙄𝘿𝙀𝙊𝙎 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅
2. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙁𝙍𝙀𝙀 ✅
3. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ✅
4. 𝘿𝙄𝙍𝙀𝘾𝙏 𝙒𝘼𝙏𝘾𝙃 𝙑𝙄𝘿𝙀𝙊𝙎 ✅
𝙏𝙊 𝘽𝙐𝙔 𝙋𝙇𝘼𝙉𝙎 𝘾𝙃𝙀𝘾𝙇 𝘽𝙐𝙏𝙏𝙊𝙉𝙎 𝘽𝙀𝙇𝙊𝙒 𝘼𝙉𝘿 𝘾𝙃𝙀𝘾𝙆 𝘿𝙀𝙈𝙊 𝘼𝙇𝙎𝙊 😍🔥.'''

# Add/edit exactly 10 plan entries here. Leave unused entries with active=False.
PLANS = [
    {
        'id': 1, 'name': '𝙈𝙊𝙈 𝘼𝙉𝘿 𝙎𝙊𝙉 😍🔥 ', 'price': '49',
        'validity': '180 days', 'videos': 'As described',
        'image': 'https://ibb.co/ZRqKVvRQ', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [
'https://t.me/studyof12th/27',
'https://t.me/studyof12th/30',
'https://t.me/studyof12th/47',
'https://t.me/studyof12th/65'
        ],
   'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 𝙁𝙍𝙄𝘿𝘼𝙔 ✅.'
),
'active': True
    },
      {
        'id': 4, 'name': '𝙍!@𝙋𝙀 𝙑𝙄𝘿𝙀𝙊𝙎 💦👀 ', 'price': '69',
        'validity': '180 days', 'videos': '40000',
        'image': 'https://ibb.co/QF2v05qK', 'qr': 'https://ibb.co/gbLMg58r',
        'demos': [   
'https://t.me/studyof12th/42',
'https://t.me/studyof12th/37',
'https://t.me/studyof12th/20',
'https://t.me/studyof12th/12',
'https://t.me/studyof12th/15',
'https://t.me/studyof12th/40',
'https://t.me/studyof12th/40'
        ],
      'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 SATURDAY ✅.'
),
'active': True
    },
      {
        'id': 5, 'name': '𝘾𝙃𝙄!𝙇𝘿 𝙑𝙄𝘿!𝙀𝙊 ( 𝘾.𝙋)  🔥👀', 'price': '49',
        'validity': '180 days', 'videos': '70000+',
        'image': 'https://ibb.co/21H7BGM2', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [          
'https://t.me/studyof12th/51',
'https://t.me/studyof12th/41',
'https://t.me/studyof12th/28',
'https://t.me/studyof12th/26',
'https://t.me/studyof12th/25',
'https://t.me/studyof12th/24',
'https://t.me/studyof12th/6'
        ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 SUNDAY✅.'
),
'active': True
    },
      {
        'id': 6, 'name': '𝘽𝙃𝘼𝙄 𝘽𝙀𝙃𝘼𝙉 🔥🥵 ', 'price': '49',
        'validity': '180 days', 'videos': '67000+',
        'image': 'https://ibb.co/9kKCd6ZF', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [
'https://t.me/studyof12th/53',
'https://t.me/studyof12th/10',
'https://t.me/studyof12th/55',
'https://t.me/studyof12th/7',
'https://t.me/studyof12th/34',
'https://t.me/studyof12th/49',
'https://t.me/studyof12th/54'
        ],
      'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 MONDAY ✅.'
),
'active': True
    },
      {
        'id': 7, 'name': '𝘽𝙃𝘼𝘽𝙃𝙄 𝙑𝙄𝘿𝙀𝙊𝙎 💦👅 ', 'price': '39',
        'validity': '180 days', 'videos': '56000+',
        'image': 'https://ibb.co/HLw36KQ4', 'qr': 'https://ibb.co/4n9q8mK2',
        'demos': [
'https://t.me/studyof12th/48',
'https://t.me/studyof12th/62',
'https://t.me/studyof12th/21',
'https://t.me/studyof12th/23',
'https://t.me/studyof12th/29',
'https://t.me/studyof12th/36'
        ],
      'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 TUESDAY ✅.'
),
'active': True
    },
      {
        'id': 8, 'name': '𝘽𝘼𝘼𝙋 𝘽𝙀𝙏𝙄 🔥💦 ', 'price': '58',
        'validity': '180 days', 'videos': '30000+',
        'image': 'https://ibb.co/5X0hc5dd', 'qr': 'https://ibb.co/xK77FFDK',
        'demos': [
'https://t.me/studyof12th/60',
'https://t.me/studyof12th/59',
'https://t.me/studyof12th/58'
        ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 WEDNESDAY ✅.'
),
'active': True
    },
      {
        'id': 9, 'name': '𝙂𝙄𝙍𝙇𝙎 𝙒𝙄𝙏𝙃 𝘼𝙉!𝙈@𝙇🔥', 'price': '49',
        'validity': '180 days', 'videos': '18000+',
        'image': 'https://ibb.co/C5KZBm7f', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [
'https://t.me/studyof12th/61'
        ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 THURSDAY ✅.'
),
'active': True
    },
      {
        'id': 10, 'name': '𝗜𝗡𝗦𝗧𝗚𝗥𝗔𝗠 𝗠𝗠𝗦 𝗔𝗟𝗟 😍🔥 ', 'price': '49',
        'validity': '180 days', 'videos': '50000+',
        'image': 'https://ibb.co/Fb6S1mYg', 'qr': 'https://ibb.co/fYsgpT3c',
        'demos': [
'https://t.me/studyof12th/35',
'https://t.me/studyof12th/50',
'https://t.me/studyof12th/63',
'https://t.me/studyof12th/56',
'https://t.me/studyof12th/52'
        ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 𝙁𝙍𝙄𝘿𝘼𝙔 ✅.'
),
'active': True
    },
    {
        'id': 2, 'name': '𝙈𝙄𝙓 𝙂𝙍𝙊𝙐𝙋 70𝙆 𝙑𝙄𝘿𝙀𝙊𝙎 🥵 ', 'price': '63',
        'validity': '180 days', 'videos': '70000+',
        'image': 'https://ibb.co/qFhKnzcH', 'qr': 'https://ibb.co/tMVzjb0D',
        'demos': [
'https://t.me/studyof12th/31',
'https://t.me/studyof12th/57'
       ],
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 SATURDAY ✅.'
),
'active': True
    },
    {
        'id': 3, 'name': '🔥𝗔𝗟𝗟 𝗩𝗜𝗣 𝗠𝗘𝗚𝗔 𝗣𝗔𝗖𝗞 😍', 'price': '169',
        'validity': '180 days', 'videos': '1 lakh+ ',
        'image': 'https://ibb.co/84598K8j', 'qr': 'https://ibb.co/MDWVSzF8',
       'caption': (
    '1. 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙎𝘼𝙑𝙀 𝙄𝙉 𝙂𝘼𝙇𝙇𝙀𝙍𝙔 ✅\n'
    '2. 𝙉𝙊 𝘼𝙉𝙔 𝘼𝘿𝙎 ❌\n'
    '3. 𝙃𝙄𝙂𝙃 𝙌𝙐𝘼𝙇𝙄𝙏𝙔 𝙑𝙄𝘿𝙀𝙊𝙎 😍\n'
    '4. 𝙉𝙀𝙒 𝙑𝙄𝘿𝙀𝙊𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙀𝙑𝙀𝙍𝙔 SUNDAY ✅.'
),
'active': True
    },
]
# =================== END OF EDITABLE CONTENT =====================

# Telegram supports button styles only on some Bot API/client versions.
# We try the requested red/green/blue style sequence and gracefully fall back.
STYLE_SERIES = [
    'danger',
    'success',
    'primary',
    'danger',
    'success',
    'primary',
    'danger'
]


# =========================
# SUPPORT LINK
# =========================

SUPPORT_LINK = 'https://t.me/YOUR_SUPPORT_USERNAME'


# =========================
# BUTTON FUNCTIONS
# =========================

def button(text, data=None, url=None, style=None):
    kwargs = {'text': text}

    if data is not None:
        kwargs['callback_data'] = data

    if url is not None:
        kwargs['url'] = url

    if style:
        try:
            return InlineKeyboardButton(**kwargs, style=style)
        except (TypeError, ValueError):
            pass

    return InlineKeyboardButton(**kwargs)


def add_styled(kb, text, data=None, url=None, index=0):
    kb.add(
        button(
            text,
            data=data,
            url=url,
            style=STYLE_SERIES[index % len(STYLE_SERIES)]
        )
    )


def get_plan(pid):
    return next(
        (
            p for p in PLANS
            if p['id'] == pid and p.get('active')
        ),
        None
    )


# =========================
# SEND PHOTO OR TEXT
# =========================

def send_photo_or_text(chat_id, image, caption, reply_markup=None):
    try:
        if image:
            bot.send_photo(
                chat_id,
                image,
                caption=caption,
                reply_markup=reply_markup
            )
        else:
            bot.send_message(
                chat_id,
                caption,
                reply_markup=reply_markup
            )

    except Exception:
        log.exception(
            'Could not send configured image; sending text fallback'
        )

        bot.send_message(
            chat_id,
            caption,
            reply_markup=reply_markup
        )


# =========================
# AGE GATE
# =========================

def send_age_gate(chat_id):
    kb = InlineKeyboardMarkup()

    kb.row(
        button(
            '𝙔𝙚𝙨, 𝙄’𝙢 18+',
            'age:yes',
            style='success'
        ),
        button(
            '𝙄’𝙢 𝙣𝙤𝙩',
            'age:no',
            style='danger'
        )
    )

    send_photo_or_text(
        chat_id,
        AGE_IMAGE,
        AGE_CAPTION,
        kb
    )


# =========================
# HOME
# =========================

def send_home(chat_id):
    kb = InlineKeyboardMarkup()

    # All active plans
    for i, p in enumerate(
        [p for p in PLANS if p.get('active')]
    ):
        add_styled(
            kb,
            f"{p['name']} · ₹{p['price']}",
            f"plan:{p['id']}",
            index=i
        )

    # Demo button
    add_styled(
        kb,
        '🎬 𝘿𝙚𝙢𝙤',
        'demo_menu',
        index=0
    )

    # Support button
    add_styled(
        kb,
        '🆘 𝙎𝙪𝙥𝙥𝙤𝙧𝙩',
        url=SUPPORT_LINK,
        index=1
    )

    send_photo_or_text(
        chat_id,
        WELCOME_IMAGE,
        WELCOME_CAPTION,
        kb
    )


# =========================
# PLANS MENU
# =========================

def send_plans(chat_id):
    kb = InlineKeyboardMarkup()

    for i, p in enumerate(
        [p for p in PLANS if p.get('active')]
    ):
        add_styled(
            kb,
            f"{p['name']} · ₹{p['price']}",
            f"plan:{p['id']}",
            index=i
        )

    # Demo button
    add_styled(
        kb,
        '🎬 𝘿𝙚𝙢𝙤',
        'demo_menu',
        index=0
    )

    # Support button
    add_styled(
        kb,
        '🆘 𝙎𝙪𝙥𝙥𝙤𝙧𝙩',
        url=SUPPORT_LINK,
        index=1
    )

    bot.send_message(
        chat_id,
        '𝘾𝙝𝙤𝙤𝙨𝙚 𝙖 𝙥𝙡𝙖𝙣:',
        reply_markup=kb
    )


# =========================
# DEMO MENU
# =========================

def send_demo_menu(chat_id):
    kb = InlineKeyboardMarkup()

    bot.send_message(
        chat_id,
        '🇮🇳 𝘿𝙚𝙢𝙤 𝙙𝙚𝙠𝙝𝙣𝙚 𝙠𝙚 𝙡𝙞𝙮𝙚 𝙠𝙤𝙞 𝙥𝙡𝙖𝙣 𝙨𝙚𝙡𝙚𝙘𝙩 𝙠𝙖𝙧𝙚𝙞𝙣.\n'
        '🇬🇧 𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙚𝙡𝙚𝙘𝙩 𝙖 𝙥𝙡𝙖𝙣 𝙩𝙤 𝙫𝙞𝙚𝙬 𝙩𝙝𝙚 𝙙𝙚𝙢𝙤.'
    )

    # All active plans
    for i, p in enumerate(
        [p for p in PLANS if p.get('active')]
    ):
        add_styled(
            kb,
            f"🎬 {p['name']}",
            f"plan:{p['id']}",
            index=i
        )

    # Back button
    add_styled(
        kb,
        '🔙 𝘽𝙖𝙘𝙠',
        'home',
        index=4
    )

    bot.send_message(
        chat_id,
        '👇 𝙎𝙚𝙡𝙚𝙘𝙩 𝙖 𝙥𝙡𝙖𝙣:',
        reply_markup=kb
    )


# =========================
# PLAN DETAILS
# =========================

def send_plan(chat_id, p):
    caption = (
        f"𝙋𝙡𝙖𝙣 : {p['name']}\n\n"
        f"𝙋𝙧𝙞𝙘𝙚 - ₹{p['price']}\n"
        f"𝙑𝙖𝙡𝙞𝙙𝙞𝙩𝙮 - {p['validity']}\n"
        f"𝙑𝙞𝙙𝙚𝙤𝙨 - {p['videos']}\n\n"
        f"{p['caption']}"
    )

    kb = InlineKeyboardMarkup()

    # Buy button
    add_styled(
        kb,
        '𝘽𝙐𝙔 𝙉𝙊𝙒 💳',
        f"buy:{p['id']}",
        index=0
    )

    # Demo buttons
    demos = p.get('demos', [])

    for i, url in enumerate(demos, start=1):
        if url.startswith(('https://', 'http://')):
            add_styled(
                kb,
                f'🎬 𝘿𝙚𝙢𝙤 {i}',
                url=url,
                index=i
            )

    # Back button
    add_styled(
        kb,
        '🔙 𝘽𝙖𝙘𝙠',
        'home',
        index=4
    )

    send_photo_or_text(
        chat_id,
        p.get('image', ''),
        caption,
        kb
    )


# =========================
# PAYMENT
# =========================

def send_payment(chat_id, user_id, p):
    if not p.get('qr'):
        bot.send_message(
            chat_id,
            '𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙌𝙍 𝙞𝙨 𝙣𝙤𝙩 𝙨𝙚𝙩 𝙞𝙣 𝙘𝙤𝙙𝙚 𝙮𝙚𝙩.'
        )
        return

    kb = InlineKeyboardMarkup()

    add_styled(
        kb,
        '𝙄 𝙋𝘼𝙄𝘿 ✅',
        f"paid:{p['id']}",
        index=0
    )

    add_styled(
        kb,
        '𝘽𝘼𝘾𝙆 ⬅️',
        f"plan:{p['id']}",
        index=1
    )

    caption = (
        f"𝙋𝙖𝙮 ₹{p['price']} using this QR.\n\n"
        f"𝙎𝙩𝙚𝙥𝙨:\n"
        f"1. 𝙎𝙘𝙖𝙣 𝙩𝙝𝙚 𝙌𝙍✅.\n"
        f"2. 𝙋𝙖𝙮 𝙩𝙝𝙚 𝙚𝙭𝙖𝙘𝙩 𝙖𝙢𝙤𝙪𝙣𝙩✅.\n"
        f"3. 𝙏𝙖𝙥 ‘𝙄 𝙥𝙖𝙞𝙙’✅.\n"
        f"4. 𝙎𝙚𝙣𝙙 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩✅.\n"
        f"5. 𝙊𝙧𝙙𝙚𝙧 ID: {user_id}-{p['id']}"
    )

    send_photo_or_text(
        chat_id,
        p['qr'],
        caption,
        kb
    )


# =========================
# ORDER STATE
# =========================

pending_screenshots = {}
user_waiting_screenshot = set()


# =========================
# START
# =========================

@bot.message_handler(commands=['start'])
def start(message):
    user_waiting_screenshot.discard(
        message.from_user.id
    )
    send_age_gate(message.chat.id)


# =========================
# AGE CALLBACK
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data in ('age:yes', 'age:no')
)
def age_choice(call):
    bot.answer_callback_query(call.id)

    if call.data == 'age:no':
        kb = InlineKeyboardMarkup()

        add_styled(
            kb,
            '𝘽𝙖𝙘𝙠',
            'age:back',
            index=0
        )

        bot.send_message(
            call.message.chat.id,
            DENIED_CAPTION,
            reply_markup=kb
        )
    else:
        send_home(call.message.chat.id)


@bot.callback_query_handler(
    func=lambda c: c.data == 'age:back'
)
def age_back(call):
    bot.answer_callback_query(call.id)
    send_age_gate(call.message.chat.id)


# =========================
# HOME CALLBACK
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data == 'home'
)
def home(call):
    bot.answer_callback_query(call.id)
    send_home(call.message.chat.id)


# =========================
# PLANS CALLBACK
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data == 'plans'
)
def plans(call):
    bot.answer_callback_query(call.id)
    send_plans(call.message.chat.id)


# =========================
# DEMO CALLBACK
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data == 'demo_menu'
)
def demo_menu(call):
    bot.answer_callback_query(call.id)
    send_demo_menu(call.message.chat.id)


# =========================
# PLAN CALLBACK
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data.startswith('plan:')
)
def plan_detail(call):
    bot.answer_callback_query(call.id)

    try:
        p = get_plan(
            int(call.data.split(':')[1])
        )
    except (ValueError, IndexError):
        p = None

    if p:
        send_plan(
            call.message.chat.id,
            p
        )


# =========================
# BUY CALLBACK
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data.startswith('buy:')
)
def buy(call):
    bot.answer_callback_query(call.id)

    try:
        p = get_plan(
            int(call.data.split(':')[1])
        )
    except (ValueError, IndexError):
        p = None

    if p:
        send_payment(
            call.message.chat.id,
            call.from_user.id,
            p
        )


# =========================
# PAID CALLBACK
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data.startswith('paid:')
)
def paid(call):
    bot.answer_callback_query(call.id)

    try:
        pid = int(call.data.split(':')[1])
        p = get_plan(pid)
    except (ValueError, IndexError):
        p = None

    if not p:
        return

    user_waiting_screenshot.add(
        call.from_user.id
    )

    bot.send_message(
        call.message.chat.id,
        '𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙚𝙣𝙙 𝙩𝙝𝙚 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 ✅.'
    )

    pending_screenshots[
        call.from_user.id
    ] = {
        'plan_id': pid,
        'status': 'waiting'
    }


# =========================
# SCREENSHOT HANDLER
# =========================

@bot.message_handler(
    content_types=['photo', 'text', 'document']
)
def screenshot_handler(message):
    uid = message.from_user.id

    if uid not in user_waiting_screenshot:
        return

    if message.content_type != 'photo':
        bot.reply_to(
            message,
            '𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙖𝙨 𝙖 𝙥𝙝𝙤𝙩𝙤.'
        )
        return

    state = pending_screenshots.get(uid, {})
    pid = state.get('plan_id')

    p = get_plan(pid) if pid else None

    if not p:
        bot.reply_to(
            message,
            '𝙋𝙡𝙖𝙣 𝙞𝙣𝙛𝙤 𝙢𝙞𝙨𝙨𝙞𝙣𝙜. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙩𝙧𝙮 𝙖𝙜𝙖𝙞𝙣.'
        )
        return

    user_waiting_screenshot.discard(uid)

    file_id = message.photo[-1].file_id

    kb = InlineKeyboardMarkup()

    add_styled(
        kb,
        '𝘼𝙥𝙥𝙧𝙤𝙫𝙚',
        f'review:approve:{uid}:{pid}',
        index=1
    )

    add_styled(
        kb,
        '𝙍𝙚𝙟𝙚𝙘𝙩',
        f'review:reject:{uid}:{pid}',
        index=0
    )

    try:
        bot.send_photo(
            ADMIN_ID,
            file_id,
            caption=(
                f"𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙨𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩\n"
                f"𝙐𝙨𝙚𝙧 𝙄𝘿: {uid}\n"
                f"𝙋𝙡𝙖𝙣: {p['name']}\n"
                f"𝘼𝙢𝙤𝙪𝙣𝙩: ₹{p['price']}"
            ),
            reply_markup=kb
        )

        bot.reply_to(
            message,
            '𝙎𝙘𝙧𝙚𝙚𝙣𝙨𝙝𝙤𝙩 𝙨𝙪𝙗𝙢𝙞𝙩𝙩𝙚𝙙.'
        )

    except Exception:
        log.exception(
            'Failed sending screenshot to admin'
        )

        user_waiting_screenshot.add(uid)

        bot.reply_to(
            message,
            '𝙎𝙪𝙗𝙢𝙞𝙨𝙨𝙞𝙤𝙣 𝙛𝙖𝙞𝙡𝙚𝙙. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙩𝙧𝙮 𝙖𝙜𝙖𝙞𝙣.'
        )


# =========================
# ADMIN REVIEW
# =========================

@bot.callback_query_handler(
    func=lambda c: c.data.startswith('review:')
)
def review(call):

    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(
            call.id,
            'Not allowed',
            show_alert=True
        )
        return

    # IMPORTANT
    parts = call.data.split(':')

    if len(parts) != 4 or parts[1] not in (
        'approve',
        'reject'
    ):
        bot.answer_callback_query(
            call.id,
            'Invalid action',
            show_alert=True
        )
        return

    action = parts[1]
    uid_s = parts[2]
    pid_s = parts[3]

    try:
        uid = int(uid_s)
        pid = int(pid_s)

    except ValueError:
        bot.answer_callback_query(
            call.id,
            'Invalid order',
            show_alert=True
        )
        return

    p = get_plan(pid)

    status = (
        'approved'
        if action == 'approve'
        else 'rejected'
    )

    try:
        if action == 'approve':
            bot.send_message(
                uid,
                '𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙖𝙥𝙥𝙧𝙤𝙫𝙚𝙙. 𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪.'
            )
        else:
            bot.send_message(
                uid,
                '𝙋𝙖𝙮𝙢𝙚𝙣𝙩 𝙧𝙚𝙟𝙚𝙘𝙩𝙚𝙙. '
                '𝙋𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙖𝙙𝙢𝙞𝙣 '
                '𝙞𝙛 𝙮𝙤𝙪 𝙩𝙝𝙞𝙣𝙠 𝙩𝙝𝙞𝙨 𝙞𝙨 𝙖 𝙢𝙞𝙨𝙩𝙖𝙠𝙚.'
            )

    except Exception:
        log.exception(
            'Could not notify user %s',
            uid
        )

    bot.answer_callback_query(
        call.id,
        status.title()
    )

    try:
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )
    except Exception:
        pass

    bot.send_message(
        ADMIN_ID,
        f'𝙊𝙧𝙙𝙚𝙧 {status}: '
        f'user {uid}, '
        f'plan {p["name"] if p else pid}.'
    )


# =========================
# START BOT
# =========================

if __name__ == '__main__':
    log.info(
        'Starting fixed-config bot (no admin panel)'
    )

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )

if __name__ == '__main__':
    log.info('Starting fixed-config bot (no admin panel)')
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
